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


from algorithms.nn.feature_extraction import feature_extract
from algorithms.nn.NN_predicting_nearest_neighbour import predict_nearest_neighbour
from algorithms.nn.Update_tree import update_tree


from app.settings import DEFAULT_USERNAME


@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def generate_feature_extraction(request):
    """

    This function is to extract features
    request_params : title: String
    request_params : file_names : List (File names of DNAs)
    response : Matrix Generation Process details 

    """
    try:
        path = request.data['path']
        feature_extract(path)
    except Exception as ex:
        print(ex)
        return Response(status=HTTP_400_BAD_REQUEST)

    return Response( status=HTTP_200_OK)


