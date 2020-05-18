from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time
import os
from cluster.services import create_directory, remove_directory
from dna_storage.models import *
from algorithms.kmer.kmer_distance_calculation import kmer_forest_generation
from dsk.bin.kp import run_kmer_sh_file
from algorithms.kmer.csv_operations import text_to_csv
from app.settings import DEFAULT_USERNAME
from dna_storage.services import download_files_from_bucket, upload_file


@shared_task
def generate_kmer_forest(file_id, defaultUser):
    """
    Generate the Kmer Forest of a DNA File.
    This method runs as a background process in Celery workers consists of nine sub tasks

        1. Create directories to genrate the kmer forest
        2. Download the dna file from S3 bucket
        3. Count the kmers using dsk tool and store them in DSK_RESULTS directory
        4. Generate the CSV files to above dsk results in the CSV_RESULTS directory
        5. Generate the Kmer Forest
        6. Upload the Kmer Forest to S3 bucket
        7. Update the database
        8. Delete the directory

    """
    processStartingTime = time.time()

    dna_file = DNAFile.objects.get(id=file_id)

    print("KMer Forest Creation of " +
          str(dna_file.file_name) + " Started.")

    # process directory path ex: BASE_DIR/storage/process_id/
    kmer_directory_path = "/tmp/KmerForest/" + str(file_id) + "/"

    # dna files directory path ex: BASE_DIR/storage/process_id/DNA_SEQUNCES/
    process_dna_file_directory_path = kmer_directory_path + "DNA_SEQUNCES/"

    # dsk results directory path ex: BASE_DIR/storage/process_id/DSK_RESULTS/
    process_dsk_results_directory_path = kmer_directory_path + "DSK_RESULTS/"

    # csv results directory path ex: BASE_DIR/storage/process_id/CSV_RESULTS/
    process_csv_results_path = kmer_directory_path + "CSV_RESULTS/"

    # k-mer forests storing directory
    process_kmer_forests_path = kmer_directory_path + "kmer_forests/"

    # create a directory to the process
    create_directory(kmer_directory_path)

    # create a directory to download dna files
    create_directory(process_dna_file_directory_path)

    # create a directory to store dsk results
    create_directory(process_dsk_results_directory_path)

    # create a directory to store csv results
    create_directory(process_csv_results_path)

    # create a directory to store kmer forest
    create_directory(process_kmer_forests_path)

    # S3 bucket directory name
    if defaultUser:
        dna_directory_name = DEFAULT_USERNAME
    else:
        dna_directory_name = dna_file.directory.name

    # for every file in the process
    # download the file to a specific location

    # ex : username/dnafile.fna
    object_name = dna_directory_name + "/dna_files/" + dna_file.object_key

    # location where the file is downloaded
    location = process_dna_file_directory_path + dna_file.object_key

    downloadStartingTime = time.time()
    print(str(object_name) + " Downloading Started.")

    download_files_from_bucket(
        object_name=object_name, location=location)

    print("Time for downloading " + str(object_name),
          time.time() - downloadStartingTime)

    print("Kmer Listing Started")
    # calls the kmer_listing script to generate the dsk results
    run_kmer_sh_file(dna_sequence_path=process_dna_file_directory_path,
                     dsk_results_path=process_dsk_results_directory_path)

    print("Kmer Listing Finished")

    # conver the text file into csv
    text_to_csv(DSK_Path=process_dsk_results_directory_path,
                CSV_Path=process_csv_results_path)

    # create the kmer forest and get the kmer similarites
    kmer_count = kmer_forest_generation(csv_file_list_path=process_csv_results_path,
                                        kmer_forest_path=process_kmer_forests_path)

    kmer_forests = os.listdir(process_kmer_forests_path)

    for kmer_forest in kmer_forests:

        print(dna_directory_name)
        object_name = dna_directory_name + "/kmer_forest/" + str(kmer_forest)

        file_name = process_kmer_forests_path + str(kmer_forest)

        print(file_name)
        is_uploaded = upload_file(file_name=file_name, object_name=object_name)

        if is_uploaded:
            kmer_forest_object = KmerForest(
                dna_file=dna_file, location=object_name, kmer_count=kmer_count)
            kmer_forest_object.save()

    dna_file.is_available = True
    dna_file.save()

    remove_directory(path=kmer_directory_path)
