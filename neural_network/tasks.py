import time
from app.settings import DEFAULT_USERNAME
from app.settings import BASE_DIR

from cluster.services import *

from dna_storage.services import download_files_from_bucket,upload_file
from dna_storage.models import Directory


from neural_network.algorithms.feature_extraction_a import feature_extract
from neural_network.algorithms.feature_extraction_b import feature_extraction_b
from neural_network.algorithms.feature_extraction_c import Make_attributes
from neural_network.algorithms.NN_predicting_nearest_neighbour import predict_nearest_neighbour
from neural_network.algorithms.Update_tree import update_tree


@shared_task
def update_phylogenetic_tree(process_id,new_species_file_name, defaultUser=False):
    """
    This method runs as a background process in Celery workers consists of nine sub tasks

        1. Create directories to the processs,dna files,kmer forests and tree json object
        2. Download necessary files from S3 bucket
        3. Create feature extraction files
        4. Create ACTG count file
        5. Create Prediction_Data.csv file
        6. Update the tree
        7. Upload the tree
        8. Delete the process directory

    :param : process_id : int
    :returns : True 

    """
    processStartingTime = time.time()

    print("Phylogenetic tree updating of " +
          str(process_id) + " Started.")

    # process directory path ex: BASE_DIR/storage/process_id/
    process_directory_path = "/tmp/" + str(process_id) + "/"

    # dna files directory path ex: BASE_DIR/storage/process_id/sample_sequences/
    process_dna_file_directory_path = process_directory_path + "sample_sequences/"

    # kmer forest results directory path ex: BASE_DIR/storage/process_id/kmer_forests/
    process_kmer_forests_directory_path = process_directory_path + "kmer_forests/"

    # extracted_features_directory path ex: BASE_DIR/storage/process_id/extracted_features/
    process_extracted_features_path = process_directory_path + "extracted_features/"

    # additional_files_directory path ex: BASE_DIR/storage/process_id/additional_files/
    process_additional_files_path = process_directory_path + "additional_files/"

    # create a directory to the process
    create_directory(process_directory_path)

    # create a directory to download dna files
    create_directory(process_dna_file_directory_path)

    # create a directory to download kmer forests
    create_directory(process_kmer_forests_directory_path)

    # create a directory to store extracted features
    create_directory(process_extracted_features_path)

    # create a directory to store additional files
    create_directory(process_additional_files_path)

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

    print("Feature extraction started")
    # making the extracted feature files
    feature_extract(kmer_forests_path=process_kmer_forests_directory_path,
        extracted_features_path=process_extracted_features_path)

    print("Feature extraction Finished")

    # creating the ACTG count file
    feature_extraction_b(filePath=process_dna_file_directory_path,additional_file_path=process_additional_files_path)

    # creating the Prediction_Data.csv file
    Make_attributes(new_species_file_name,filePath=process_dna_file_directory_path,
        additional_files=process_additional_files_path,kmerACTGFilePath=process_extracted_features_path)

    #update the tree
    updated_tree=update_tree(additional_files=process_additional_files_path)

    # update the process status
    process.status = 2
    process.save()

    object_name = "phylogenetic_trees/" + str(process_id) + "/" + str(updated_tree)

    file_name = str(updated_tree)

    is_uploaded = upload_file(file_name=file_name, object_name=object_name)

    if is_uploaded:
        #save the tree code
        return True

    # delete the process floder
    # return True if success

    is_removed = remove_directory(path=process_directory_path)

    if is_removed:
        print("Update Tree process of process id=" +
              str(process_id) + " ended")
        print("Time taken for the process=", time.time() - processStartingTime)
        return is_removed
    else:
        return is_removed
