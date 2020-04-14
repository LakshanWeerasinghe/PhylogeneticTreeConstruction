from __future__ import absolute_import, unicode_literals

# djanco
from django.contrib.auth.models import User

# python3
import os
import shutil
import sys

# moules
from algorithms import lsh
from dna_storage.models import Directory
from dna_storage.services import download_files_from_bucket
from app.settings import BASE_DIR

# celery
from celery import shared_task

# other
from .models import Process, Result
from .services import create_directory, remove_directory


@shared_task
def generate_distance_matrix_using_lsh_task(process_id):
    """
    This method runs as a background process in Celery workers consists of six sub tasks

        1. Create directories to the processs and dna files
        2. Download dna files from S3 bucket 
        3. Generate Distance Matrix
        4. Store matrix in Results model
        5. Update the Process model
        6. Delete the processs directory

    :param : process_id : string
    :returns : True if not False

    """

    # process directory path ex: BASE_DIR/storage/process_id/
    process_directory_path = BASE_DIR + "/storage/" + str(process_id) + "/"

    # dna files directory path ex: BASE_DIR/storage/process_id/DNA_SEQUNCES/
    process_dna_file_directory_path = process_directory_path + "DNA_SEQUNCES/"

    # create a directory to the process
    create_directory(process_directory_path)

    # create a directory to download dna files
    create_directory(process_dna_file_directory_path)

    # process instance
    process = Process.objects.get(id=process_id)

    # S3 bucket directory name
    dna_directory = Directory.objects.get(user=process.user)

    dna_files = process.dna_files.all()

    # create a dictonary
    # key : object key without extension
    # value : file name (spieces name)
    file_dict = {}

    # for every file in the process
    # download the file to a specific location
    for dna in dna_files:

        # ex : username/dnafile.fna
        object_name = dna_directory.name + "/" + dna.object_key

        # location where the file is downloaded
        location = process_dna_file_directory_path + dna.object_key

        download_files_from_bucket(
            object_name=object_name, location=location)

        file_dict[dna.object_key[:-4]] = dna.file_name

    # genreate matrix
    # process id
    result_matrix = lsh.main(process_id, file_dict)

    # save results in results table
    result = Result(process=process, result=result_matrix)
    result.save()

    # update the process status
    process.status = 2
    process.save()

    # delete the process floder
    # return True if success
    return remove_directory(path=process_directory_path)