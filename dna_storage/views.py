#django
from django.shortcuts import render

#rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

#other
from .services import create_preassinged_url


# Todo
# 1. give the aws s3 url to upload the dna sequences
# 2. get the file deatils of the uploaded files
# 3. give the default storage files
# 4. view users own storage details


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_dna_sequence_upload_url(request):

    user = request.user

    #query from the db to get the url
    #serve the url

    object_name =  request.data['object_name']
    url = create_preassinged_url(object_name)

    if url is None :
        return Response("Error Occord", status=HTTP_400_BAD_REQUEST)

    return Response(url, status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_dna_file_details(request):

    #user
    #update db with the users dna storage
    #return the response

    return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dna_bank_files(request):

    #query from the db and send the response

    return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_dna_file_details(request):

    #user
    #query from db and return the responses

    return Response(status=HTTP_200_OK)