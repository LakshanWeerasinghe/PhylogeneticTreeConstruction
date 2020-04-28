from __future__ import absolute_import, unicode_literals

# djanco
from django.contrib.auth.models import User

# python3
import os
import shutil
import sys
import subprocess

# moules
from algorithms.lsh import lsh
from algorithms.lsh.kmedoid_clustering_LSH import start_kemedoid
from dna_storage.models import Directory
from dna_storage.services import download_files_from_bucket, upload_file
from app.settings import BASE_DIR
from algorithms.kmer.csv_operations import text_to_csv
from algorithms.kmer.kmer_distance_calculation import kmer_distance_main
from algorithms.kmer.kmedoid_clustering_kmer import start_kmedoid_kmer

# celery
from celery import shared_task

# other
from .models import *
from .services import create_directory, remove_directory
import time

from dsk.bin.kp import run_kmer_sh_file
from app.settings import DEFAULT_USERNAME


@shared_task
def generate_distance_matrix_using_lsh_task(process_id, defaultUser=False):
    """
    This method runs as a background process in Celery workers consists of six sub tasks

        1. Create directories to the processs and dna files
        2. Download dna files from S3 bucket
        3. Generate Distance Matrix
        4. Store matrix in Results model
        5. Update the Process model
        6. Delete the processs directory

    :param : process_id : int
    :returns : True if not False

    """
    processStartingTime = time.time()

    print("Distance Matrix creation process of process id=" +
          str(process_id) + " using LSH started ")

    # process directory path ex: BASE_DIR/tmp/process_id/
    process_directory_path = "/tmp/" + str(process_id) + "/"

    # dna files directory path ex: BASE_DIR/storage/process_id/DNA_SEQUNCES/
    process_dna_file_directory_path = process_directory_path + "DNA_SEQUNCES/"

    # create a directory to the process
    create_directory(process_directory_path)

    # create a directory to download dna files
    create_directory(process_dna_file_directory_path)

    # process instance
    process = MatrixProcess.objects.get(id=process_id)

    # S3 bucket directory name
    if defaultUser:
        dna_directory_name = DEFAULT_USERNAME
    else:
        dna_directory = Directory.objects.get(user=process.user)
        dna_directory_name = dna_directory.name

    dna_files = process.dna_files.all()

    # create a dictonary
    # key : object key without extension
    # value : file name (spieces name)
    file_dict = {}

    print(dna_files)
    # for every file in the process
    # download the file to a specific location
    for dna in dna_files:

        # ex : username/dnafile.fna
        object_name = dna_directory_name + "/" + dna.object_key

        # location where the file is downloaded
        location = process_dna_file_directory_path + dna.object_key

        downloadStartingTime = time.time()
        print(str(object_name) + " Downloading Started.")

        download_files_from_bucket(
            object_name=object_name, location=location)

        print("Time for downloading " + str(object_name),
              time.time() - downloadStartingTime)

        file_dict[dna.object_key[:-4]] = dna.file_name

    # genreate matrix
    # process id
    lsh_simialarities = lsh.main(process_id, file_dict)

    # save results in results table
    result = DNASimilaritiesResult(
        process=process, result=lsh_simialarities)
    result.save()

    # update the process status
    process.status = 2
    process.save()

    # delete the process floder
    # return True if success

    is_removed = remove_directory(path=process_directory_path)

    if is_removed:
        print("Distance Matrix creation process of process id=" +
              str(process_id) + " using LSH ended")
        print("Time taken for the process=", time.time() - processStartingTime)
        return is_removed
    else:
        return is_removed


@shared_task
def generate_tree_using_lsh_kmedoid(process_id, result_id):
    """
    This method runs as a background task of Celery workers this consist of 3 sub tasks
        1. Get the LSH similarities from the database
        2. Generate the Phylogenetic Tree
        3. Save the Tree result in the database
        4. Update the process status

    :param : process_id : int (Process id of the Phylogenetic Tree Creation Process)
    :param : result_id : int (Result id of the Matrix Process)
    :return : True

    """

    processStartingTime = time.time()

    print("Tree Generation process of process id=" +
          str(process_id) + " using LSH Clustering started.")

    process = PhylogeneticTreeProcess.objects.get(id=process_id)

    # get the result from database
    lsh_result = DNASimilaritiesResult.objects.get(id=result_id)

    # convert the string of lsh similarities into list of similarities
    lsh_similarities = lsh_result.result.split("\n")

    # remove the last element
    lsh_similarities = lsh_similarities[:-1]

    # generate the tree
    tree_dict = start_kemedoid(lsh_similarity_result=lsh_similarities)

    # save the result in the database
    tree_result = PhylogeneticTreeResult(process=process, tree=tree_dict)
    tree_result.save()

    # update the process status
    process.status = 2
    process.save()

    print("Tree Generation process of process id=" +
          str(process_id) + " using LSH Clustering has ended.")
    print("Time taken for the process=", time.time() - processStartingTime)
    return True


@shared_task
def generate_distance_matrix_using_kmer_task(process_id, defaultUser=False):
    """
    This method runs as a background process in Celery workers consists of nine sub tasks

        1. Create directories to the processs and dna files
        2. Download dna files from S3 bucket
        3. Count the kmers using dsk tool and store them in DSK_RESULTS directory
        4. Generate the CSV files to above dsk results in the CSV_RESULTS directory
        5. Generate the similarites of the DNA files
        6. Store the results in the table
        7. Update the process status
        8. Upload the Kmer Forest to S3 bucket
        9. Delete the process directory

    :param : process_id : int
    :returns : True 

    """
    processStartingTime = time.time()

    print("Kmer Similarities counting process of process id=" +
          str(process_id) + " Started.")

    # process directory path ex: BASE_DIR/storage/process_id/
    process_directory_path = "/tmp/" + str(process_id) + "/"

    # dna files directory path ex: BASE_DIR/storage/process_id/DNA_SEQUNCES/
    process_dna_file_directory_path = process_directory_path + "DNA_SEQUNCES/"

    # dsk results directory path ex: BASE_DIR/storage/process_id/DSK_RESULTS/
    process_dsk_results_directory_path = process_directory_path + "DSK_RESULTS/"

    # csv results directory path ex: BASE_DIR/storage/process_id/CSV_RESULTS/
    process_csv_results_path = process_directory_path + "CSV_RESULTS/"

    # k-mer forests storing directory
    process_kmer_forests_path = process_directory_path + "kmer_forests/"

    # create a directory to the process
    create_directory(process_directory_path)

    # create a directory to download dna files
    create_directory(process_dna_file_directory_path)

    # create a directory to store dsk results
    create_directory(process_dsk_results_directory_path)

    # create a directory to store csv results
    create_directory(process_csv_results_path)

    # create a directory to store kmer forest
    create_directory(process_kmer_forests_path)

    # process instance
    process = MatrixProcess.objects.get(id=process_id)

    # S3 bucket directory name
    if defaultUser:
        dna_directory_name = DEFAULT_USERNAME
    else:
        dna_directory = Directory.objects.get(user=process.user)
        dna_directory_name = dna_directory.name

    dna_files = process.dna_files.all()

    # create a dictonary
    # key : object key without extension
    # value : file name (spieces name)
    file_dict = {}

    print(dna_files)
    # for every file in the process
    # download the file to a specific location
    for dna in dna_files:

        # ex : username/dnafile.fna
        object_name = dna_directory_name + "/" + dna.object_key

        # location where the file is downloaded
        location = process_dna_file_directory_path + dna.object_key

        downloadStartingTime = time.time()
        print(str(object_name) + " Downloading Started.")

        download_files_from_bucket(
            object_name=object_name, location=location)

        print("Time for downloading " + str(object_name),
              time.time() - downloadStartingTime)

        file_dict[dna.object_key[:-4]] = dna.file_name

        print(object_name)

    print("Kmer Listing Started")
    # calls the kmer_listing script to generate the dsk results
    run_kmer_sh_file(dna_sequence_path=process_dna_file_directory_path,
                     dsk_results_path=process_dsk_results_directory_path)

    print("Kmer Listing Finished")

    # conver the text file into csv
    text_to_csv(DSK_Path=process_dsk_results_directory_path,
                CSV_Path=process_csv_results_path)

    # create the kmer forest and get the kmer similarites
    kmer_similarities = kmer_distance_main(csv_file_list_path=process_csv_results_path,
                                           kmer_forest_path=process_kmer_forests_path, file_dict=file_dict)

    # save results in results table
    result = DNASimilaritiesResult(process=process, result=kmer_similarities)
    result.save()

    # update the process status
    process.status = 2
    process.save()

    kmer_forests = os.listdir(process_kmer_forests_path)

    for kmer_forest in kmer_forests:

        object_name = "kmer_forests/" + \
            str(process_id) + "/" + str(kmer_forest)

        file_name = process_kmer_forests_path + str(kmer_forest)

        is_uploaded = upload_file(file_name=file_name, object_name=object_name)

        if is_uploaded:
            kmer_forest_object = KMerForestResult(
                process=process, result_locaion=object_name)
            kmer_forest_object.save()

    # delete the process floder
    # return True if success

    is_removed = remove_directory(path=process_directory_path)

    if is_removed:
        print("Distance Matrix creation process of process id=" +
              str(process_id) + " using Kmer ended")
        print("Time taken for the process=", time.time() - processStartingTime)
        return is_removed
    else:
        return is_removed


@shared_task
def generate_tree_using_kmer_kmedoid(process_id, result_id):
    """
    This method runs as a background task of Celery workers this consist of four sub tasks
        1. Get the Kmer similarities from the database
        2. Generate the Phylogenetic Tree
        3. Save the Tree result in the database
        4. Update the process status

    :param : process_id : int (Process id of the Tree Creation Process)
    :param : result_id : int (Result id of the LSH distance matrix Process)
    :return : True

    """

    processStartingTime = time.time()

    print("Tree Generation process of process id=" +
          str(process_id) + " using Kmer Clustering started.")

    process = PhylogeneticTreeProcess.objects.get(id=process_id)

    # get the result from database
    kmer_result = DNASimilaritiesResult.objects.get(id=result_id)

    # convert the string of kmer similarities into list of similarities
    kmer_similarites = kmer_result.result.split("\n")

    # remove the last element
    kmer_similarites = kmer_similarites[:-1]

    # generate the tree
    tree_dict = start_kmedoid_kmer(kmer_similarity_result=kmer_similarites)

    # save the result in the database
    tree_result = PhylogeneticTreeResult(process=process, tree=tree_dict)
    tree_result.save()

    # update the process status
    process.status = 2
    process.save()

    print("Tree Generation process of process id=" +
          str(process_id) + " using Kmer Clustering has ended.")
    print("Time taken for the process=", time.time() - processStartingTime)
    return True
