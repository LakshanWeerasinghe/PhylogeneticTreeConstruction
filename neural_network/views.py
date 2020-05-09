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
#from .models import *

# serializers
#from .serializers import *
#import json

from app.settings import DEFAULT_USERNAME


@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def update_tree(request):
    """

    This function is to update a tree
    request_params : title: String
    request_params : file_names : List (File names of DNA fna files)
    request_params : file_names : List (File names of kmer_forests)
    request_params : previous tree json object
    response : Matrix Generation Process details 

    """

    return Response( status=HTTP_200_OK)


