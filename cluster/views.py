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

# serializers
from .serializers import *
import json

# tasks
from .tasks import *

from algorithms.lsh.kmedoid_clustering_LSH import start_kemedoid
from algorithms.distance_matrix import distanceMatrixGenerator

from dsk.bin.kp import run_kmer_sh_file
from app.settings import DEFAULT_USERNAME


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

    else:
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

    # user instance
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

    if process_type == "LSH":
        process = MatrixProcess(title=title, type=1, status=1, user=user)

        try:
            process.save()
            for dna in dna_files:
                process.dna_files.add(dna)

            # clls the celery task
            generate_distance_matrix_using_lsh_task.delay(process.id)
        except Exception as ex:
            print(ex)
            return Response(status=HTTP_400_BAD_REQUEST)

        return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)

    else:
        process = MatrixProcess(title=title, type=2, status=1, user=user)

        try:
            process.save()
            for dna in dna_files:
                process.dna_files.add(dna)

            # clls the celery task
            generate_distance_matrix_using_kmer_task.delay(process.id)
        except Exception as ex:
            print(ex)
            return Response(status=HTTP_400_BAD_REQUEST)

        return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def phylogenetic_tree_generate_view(request):
    """

    This function is to create Phylogenetic Tree creation Process For a User 
    request_params : title: String
    request_params : file_names : List (File names of DNAs)
    response : Matrix Generation Process details 

    """

    result_id = request.data["result_id"]
    title = request.data["title"]
    process_type = request.data["type"]

    serializer = TreeCreationRequestSerializer(data=request.data)

    if serializer.is_valid():
        # user instance
        user = User.objects.get(username=request.user)
        similarities_result = DNASimilaritiesResult(id=result_id)

        if process_type == "LSH":

            # create a new process and save
            process = PhylogeneticTreeProcess(title=title, type=1, status=1,
                                              user=user, similarities_result=similarities_result)
            process.save()

            # add the result to the Celery
            generate_tree_using_lsh_kmedoid.delay(
                process_id=process.id, result_id=result_id)

            return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)
        else:
            # create a new process and save
            process = PhylogeneticTreeProcess(
                title=title, type=2, status=1, user=user, similarities_result=similarities_result)
            process.save()

            # add the result to the Celery
            generate_tree_using_kmer_kmedoid.delay(
                process_id=process.id, result_id=result_id)

            return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)
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

    serializer = MatrixResultRequestSerializer(data=request.data)
    if serializer.is_valid():
        process = MatrixProcess.objects.get(id=process_id)
        result = DNASimilaritiesResult.objects.get(process=process)
        result_similarities = result.result.split("\n")
        result_matrix = distanceMatrixGenerator(result_similarities[:-1])
        response = {}

        response["process"] = process.get_process_details_as_dict()
        response["result_id"] = result.id
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

    serializer = TreeResultRequestSerializer(data=request.data)
    if serializer.is_valid():
        process = PhylogeneticTreeProcess.objects.get(id=process_id)
        tree_result = PhylogeneticTreeResult.objects.get(process=process)

        response = {}

        response["process"] = process.get_process_details_as_dict()
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
        tree_proccess_list.append(process.get_process_details_as_dict())

    response = {"matrix_processes": matrix_process_list,
                "tree_processes": tree_proccess_list}

    return Response(response, status=HTTP_200_OK)


@api_view(["GET"])
def test_view(request):

    # result = Result.objects.get(id=2)
    # result_2 = result.result.split("\n")

    # final_result = start_kemedoid(result_2[:-1])

    # r = distanceMatrixGenerator(result_2[:-1])

    # process = Process.objects.get(id=3)

    # print(process)
    # tree = TreeResult(process=process, tree=final_result)
    # print(tree)
    # tree.save()

    run_kmer_sh_file("kfmakdm", "jandjfnj")
    return Response()
