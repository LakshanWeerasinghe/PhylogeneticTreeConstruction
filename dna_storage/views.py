# django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View

# rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# other
from .services import create_preassinged_url
from .models import Directory, DNAFile
from .serializers import DNAFileSerializer, DNAFileUploadedSerializer
from app.settings import DEFAULT_USERNAME
from dna_storage.tasks import generate_kmer_forest


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_dna_sequence_upload_url_view(request):
    """ 
    Get the preassinged url to upload dna files 

    :request param : file_name : String
    :request param : object_key : String 
    :request param : size : Integer

    """

    data = request.data

    user = User.objects.get(username=request.user)
    directory = Directory.objects.get(user=user)

    directory_name = getattr(directory, 'name')
    data["directory"] = getattr(directory, 'id')

    dna_file_serializer = DNAFileSerializer(data=data)

    # validate request
    if dna_file_serializer.is_valid():

        directory_full_path = directory_name + "/dna_files"

        # get url using boto3
        url = create_preassinged_url(
            directory_name=directory_full_path, object_name=data['object_key'])

        if not url is None:
            dna_file_serializer.save()

            return Response({"url": url}, status=HTTP_200_OK)
    else:
        return Response(dna_file_serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dna_file_uploaded_view(request):
    """
    Update the is_avilable field of DNAFile if uploading sucess else delete the DNAFile

    :request param : file_name : String
    :is_uploaded : 


    """

    data = request.data

    user = User.objects.get(username=request.user)
    directory = Directory.objects.get(user=user)

    directory_name = getattr(directory, 'name')
    data["directory"] = getattr(directory, 'id')

    dna_file_uploaded_serializer = DNAFileUploadedSerializer(data=data)

    # validate request
    if dna_file_uploaded_serializer.is_valid():

        file_name = data['file_name']
        dna_file_instance = DNAFile.objects.get(
            file_name=file_name, directory=directory)

        if data['is_uploaded']:
            if user.username == DEFAULT_USERNAME:
                generate_kmer_forest.delay(dna_file_instance.id, True)
            else:
                generate_kmer_forest.delay(dna_file_instance.id, False)
        else:
            dna_file_instance.delete()

        return Response(status=HTTP_200_OK)
    else:
        return Response(dna_file_uploaded_serializer.errors,
                        status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dna_bank_files(request):
    """ Request to get the default DNA Files. """

    user = User.objects.get(username=DEFAULT_USERNAME)
    directory = Directory.objects.get(user=user)

    dna_files = []

    dna_files_query_set = DNAFile.objects.filter(
        directory=directory, is_available=True)

    for dna_file in dna_files_query_set:
        dna_files.append(dna_file.get_file_details())

    response = {"dna_files": dna_files}

    return Response(response, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_dna_file_details(request):
    """ Request to get the DNA Files of the authenticated user. """

    user = User.objects.get(username=request.user)
    directory = Directory.objects.get(user=user)

    dna_files = []

    dna_files_query_set = DNAFile.objects.filter(
        directory=directory, is_available=True)

    for dna_file in dna_files_query_set:
        dna_files.append(dna_file.get_file_details())

    response = {"dna_files": dna_files}

    return Response(response, status=HTTP_200_OK)
