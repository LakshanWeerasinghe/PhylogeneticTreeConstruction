# dajnago
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.forms.models import model_to_dict


# rest framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# models
from dna_storage.models import DNAFile, Directory
from .models import *
from neural_network.models import *

# serializers
from .serializers import *
import json

# tasks
from .tasks import *

from algorithms.lsh.kmedoid_clustering_LSH import start_kemedoid
from algorithms.distance_matrix import distanceMatrixGenerator

from dsk.bin.kp import run_kmer_sh_file
from app.settings import DEFAULT_USERNAME
from cluster.util import *


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_distance_matrix_using_default_files_view(request):
    """

    This function is to create Distance Matrix Generation Process For a User from Default DNA Files
    request_params : title: String
    request_params : file_names : List (File names of DNAs)
    response : Matrix Generation Process details 

    """

    # list to store dna file instances
    dna_files = []

    title = request.data["title"]

    process_type = request.data["type"]

    # list of dna file names
    dna_files_names = request.data["file_names"]

    # user instance
    user = User.objects.get(username=DEFAULT_USERNAME)

    # directory instance
    directory = Directory.objects.get(user=user)

    for file_name in dna_files_names:
        dna_file = None
        try:
            dna_file = DNAFile.objects.get(
                file_name=file_name, is_available=True, directory=directory)
        except ObjectDoesNotExist:
            error = file_name + " File Doesn't Exist!"
            return Response({"error": error}, status=HTTP_400_BAD_REQUEST)
        else:
            dna_files.append(dna_file)

    # create the process and stores in the database
    # generate celery task and
    # add it to the RabbitMQ

    if process_type == "LSH":
        process = MatrixProcess(title=title, type=1, status=1, user=user)

        try:
            process.save()
            for dna in dna_files:
                process.dna_files.add(dna)

            # clls the celery task
            generate_distance_matrix_using_lsh_task.delay(
                process.id, defaultUser=True)
        except Exception as ex:
            print(ex)
            return Response(status=HTTP_400_BAD_REQUEST)

        return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)

    elif process_type == "KMER":
        process = MatrixProcess(title=title, type=2, status=1, user=user)

        try:
            process.save()
            for dna in dna_files:
                process.dna_files.add(dna)

            # clls the celery task
            generate_distance_matrix_using_kmer_task.delay(
                process.id, defaultUser=True)
        except Exception as ex:
            print(ex)
            return Response(status=HTTP_400_BAD_REQUEST)

        return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)
    else:
        return Response({"error": "Wrong process type."}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_distance_matrix_view(request):
    """

    This function is to create Distance Matrix Generation Process For a User for his own DNA files
    request_params : title: String
    request_params : file_names : List (File names of DNAs)
    response : Matrix Generation Process details 

    """

    # list to store dna file instances
    dna_files = []

    title = request.data["title"]

    process_type = request.data["type"]

    # list of dna file names
    dna_files_names = request.data["file_names"]

    is_default_user = request.data["is_default_user"]

    data = {
        "title": title,
        "process_type": process_type,
        "is_default_user": is_default_user
    }

    serializer = MatrixCreationProcessSerializer(data=data)

    if serializer.is_valid():
        if is_default_user:
            user = User.objects.get(username=DEFAULT_USERNAME)
        else:
            user = User.objects.get(username=request.user)

        # directory instance
        directory = Directory.objects.get(user=user)

        for file_name in dna_files_names:
            dna_file = None
            try:
                dna_file = DNAFile.objects.get(
                    file_name=file_name, is_available=True, directory=directory)
            except ObjectDoesNotExist:
                error = file_name + " File Doesn't Exist!"
                return Response({"error": error}, status=HTTP_400_BAD_REQUEST)
            else:
                dna_files.append(dna_file)

        # create the process and stores in the database
        # generate celery task and
        # add it to the RabbitMQ

        user1 = User.objects.get(username=request.user)
        if process_type == "LSH":
            process = MatrixProcess(title=title, type=1, status=1, user=user1)

            try:
                process.save()
                for dna in dna_files:
                    process.dna_files.add(dna)

                # clls the celery task
                generate_distance_matrix_using_lsh_task.delay(
                    process.id, is_default_user)
            except Exception as ex:
                print(ex)
                return Response(status=HTTP_400_BAD_REQUEST)

            return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)

        elif process_type == "KMER":
            process = MatrixProcess(title=title, type=2, status=1, user=user1)

            try:
                process.save()
                for dna in dna_files:
                    process.dna_files.add(dna)

                # clls the celery task
                generate_distance_matrix_using_kmer_task.delay(
                    process.id, is_default_user)
            except Exception as ex:
                print(ex)
                return Response(status=HTTP_400_BAD_REQUEST)

            return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)
    else:
        return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def phylogenetic_tree_generate_view(request):
    """

    This function is to create Phylogenetic Tree creation Process For a User 
    request_params : title: String
    request_params : file_names : List (File names of DNAs)
    response : Matrix Generation Process details 

    """

    matrix_process_id = request.data["matrix_process_id"]
    title = request.data["title"]
    process_type = request.data["type"]

    data = request.data
    data["username"] = str(request.user)

    serializer = TreeCreationRequestSerializer(data=data)

    if serializer.is_valid():
        # user instance
        user = User.objects.get(username=request.user)
        matrix_process = MatrixProcess.objects.get(id=matrix_process_id)

        process = PhylogeneticTreeProcess(
            title=title, type=1, status=1, user=user)
        process.save()

        if process_type == "LSH":

            tree_creation_process = PhylogeneticTreeCreation(
                type=1, process=process, matrix_process=matrix_process)
            tree_creation_process.save()

            # add the result to the Celery
            generate_tree_using_lsh_kmedoid.delay(
                process_id=process.id)

        else:
            # create a new process and save
            tree_creation_process = PhylogeneticTreeCreation(
                type=2, process=process, matrix_process=matrix_process)
            tree_creation_process.save()

            # add the result to the Celery
            generate_tree_using_kmer_kmedoid.delay(
                process_id=process.id)

        process_details = {
            "process_id": process.id,
            "title": process.title,
            "process_type":  TreeProcessType.get_key(process.type),
            "status": ProcessStatusTypes.get_key(process.status),
            "method": ProcessTypes.get_key(tree_creation_process.type)
        }

        return Response({"process": process_details}, status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_process_matrix_result_view(request):
    """

    This function is to get the Distance Matrix of a Distance Matrix creation Process
    request_params : process_id(Id of the Distance Matrix creation process)
    response : process & result details 

    """

    process_id = request.data['process_id']
    username = request.user

    data = request.data
    data["username"] = str(username)

    serializer = MatrixResultRequestSerializer(data=data)
    if serializer.is_valid():
        process = MatrixProcess.objects.get(id=process_id)
        result = DNASimilaritiesResult.objects.get(process=process)
        result_similarities = result.result.split("\n")
        result_matrix = distanceMatrixGenerator(result_similarities[:-1])
        response = {}

        response["process"] = process.get_process_details_as_dict()
        response["matrix_result_id"] = result.id
        response["matrix"] = result_matrix

        return Response(response, status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_process_tree_result_view(request):
    """

    This function is to get the Phylogenetric Tree of a Phylogenetic Tree creation Process
    request_params : process_id(Id of the Phylogenetic Tree creation process)
    response : process & result details 

    """

    process_id = request.data['process_id']
    username = request.user

    data = request.data
    data["username"] = str(username)

    serializer = TreeResultRequestSerializer(data=data)
    if serializer.is_valid():
        process = PhylogeneticTreeProcess.objects.get(id=process_id)
        tree_result = PhylogeneticTreeResult.objects.get(process=process)

        response = {
            "process_id": process.id,
            "title": process.title,
            "process_type": TreeProcessType.get_key(process.type),
            "status": ProcessStatusTypes.get_key(process.status)
        }

        dna_files = []
        tree_creation = PhylogeneticTreeCreation.objects.get(process=process)
        dna_objects = tree_creation.matrix_process.dna_files.all()

        for dna in dna_objects:
            check_default = dna
            dna_files.append(dna.file_name)

        response["method"] = ProcessTypes.get_key(tree_creation.type)
        if process.type == 2:
            updated_tree = PhylogeneticTreeUpdate.objects.get(process=process)
            dnas_updated = updated_tree.dna_files.all()
            for dna in dnas_updated:
                dna_files.append(dna.file_name)

        if check_default.directory.name == DEFAULT_USERNAME:
            response["is_default_user"] = True
        else:
            response["is_default_user"] = False

        response["file_names"] = dna_files
        response["result_id"] = tree_result.id
        response["tree"] = tree_result.tree

        return Response(response, status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_processes_view(request):
    """

    This function is to get all the processes realated to a user.
    response : matrix_process list and tree_process list

    """

    # user instance
    user = User.objects.get(username=request.user)
    matrix_processes = MatrixProcess.objects.filter(user=user)
    tree_processes = PhylogeneticTreeProcess.objects.filter(user=user)

    matrix_process_list = []
    tree_proccess_list = []
    for process in matrix_processes:
        matrix_process_list.append(process.get_process_details_as_dict())

    for process in tree_processes:
        tree_creation = PhylogeneticTreeCreation.objects.get(process=process)

        process_details = {
            "process_id": process.id,
            "title": process.title,
            "process_type": TreeProcessType.get_key(process.type),
            "status": process.status,
        }
        process_details["method"] = ProcessTypes.get_key(tree_creation.type)

        tree_proccess_list.append(process_details)

    response = {"matrix_processes": matrix_process_list,
                "tree_processes": tree_proccess_list}

    return Response(response, status=HTTP_200_OK)
