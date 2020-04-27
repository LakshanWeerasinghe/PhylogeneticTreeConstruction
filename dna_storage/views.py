# django
from django.shortcuts import render
from django.contrib.auth.models import User

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

# Todo
# 1. give the aws s3 url to upload the dna sequences - Done
# 2. get the file deatils of the uploaded files
# 3. give the default storage files
# 4. view users own storage details


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_dna_sequence_upload_url_view(request):

    data = request.data

    user = User.objects.get(username=request.user)
    directory = Directory.objects.get(user=user)

    directory_name = getattr(directory, 'name')
    data["directory"] = getattr(directory, 'id')

    dna_file_serializer = DNAFileSerializer(data=data)

    if dna_file_serializer.is_valid():

        url = create_preassinged_url(
            directory_name=directory_name, object_name=data['object_key'])

        if not url is None:
            dna_file_serializer.save()

            return Response({"url": url}, status=HTTP_200_OK)
    else:
        return Response(dna_file_serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dna_file_uploaded_view(request):

    data = request.data

    dna_file_uploaded_serializer = DNAFileUploadedSerializer(data=data)
    user = User.objects.get(username=request.user)
    directory = Directory.objects.get(user=user)

    if dna_file_uploaded_serializer.is_valid():

        file_name = data['file_name']
        dna_file_instance = DNAFile.objects.get(
            file_name=file_name, directory=directory)
        if data['is_uploaded'] == 1:
            dna_file_instance.is_available = True
            dna_file_instance.save()
        else:
            dna_file_instance.delete()

        return Response(status=HTTP_200_OK)
    else:
        return Response(dna_file_uploaded_serializer.errors,
                        status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dna_bank_files(request):

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

    user = User.objects.get(username=request.user)
    directory = Directory.objects.get(user=user)

    dna_files = []

    dna_files_query_set = DNAFile.objects.filter(
        directory=directory, is_available=True)

    for dna_file in dna_files_query_set:
        dna_files.append(dna_file.get_file_details())

    response = {"dna_files": dna_files}

    return Response(response, status=HTTP_200_OK)
