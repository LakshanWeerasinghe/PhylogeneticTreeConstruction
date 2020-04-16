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
from .models import Process, Result, TreeResult

# serializers
from .serializers import MatrixResultRequestSerializer, TreeResultRequestSerializer

import json

# tasks
from .tasks import generate_distance_matrix_using_lsh_task, generate_tree_using_lsh_kmedoid

from algorithms.lsh.kmedoid_clustering_LSH import start_kemedoid
from algorithms.distance_matrix import distanceMatrixGenerator


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_distance_matrix_using_lsh_view(request):

    # list to store dna file instances
    dna_files = []

    title = request.data["title"]

    # list of dna file names
    dna_files_names = request.data["file_names"]

    # user instance
    user = User.objects.get(username=request.user)

    # directory instance
    directory = Directory.objects.get(user=user)

    for file_name in dna_files_names:
        dna_file = None
        try:
            dna_file = DNAFile.objects.get(file_name=file_name)
        except ObjectDoesNotExist:
            error = file_name + " File Doesn't Exist!"
            return Response({"error": error}, status=HTTP_400_BAD_REQUEST)
        else:
            dna_files.append(dna_file)

    # create the process and stores in the database
    # generate celery task and
    # add it to the RabbitMQ
    process = Process(title=title, type=1, method=1, status=1, user=user)

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_tree_using_lsh_view(request):

    result_id = request.data["result_id"]
    title = request.data["title"]

    # user instance
    user = User.objects.get(username=request.user)

    # create a new process and save
    process = Process(title=title, type=2, method=2, status=1, user=user)
    process.save()

    # add the result to the Celery
    generate_tree_using_lsh_kmedoid.delay(
        process_id=process.id, result_id=result_id)

    return Response({"process": process.get_process_details_as_dict()}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_process_matrix_result_view(request):

    process_id = request.data['process_id']

    serializer = MatrixResultRequestSerializer(data=request.data)
    if serializer.is_valid():
        process = Process.objects.get(id=process_id)
        result = Result.objects.get(process=process)
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

    process_id = request.data['process_id']

    serializer = TreeResultRequestSerializer(data=request.data)
    if serializer.is_valid():
        process = Process.objects.get(id=process_id)
        tree_result = TreeResult.objects.get(process=process)

        response = {}

        response["process"] = process.get_process_details_as_dict()
        response["result_id"] = tree_result.id
        response["tree"] = tree_result.tree

        return Response(response, status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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

    tree = TreeResult.objects.get(id=2)
    print(tree.tree)
    return Response(tree.tree)
