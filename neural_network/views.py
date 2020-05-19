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
from .models import *
from dna_storage.models import *
from cluster.models import *

from .seializers import PhylogeneticTreeUpdationRequest
# serializers
#from .serializers import *
#import json

from app.settings import DEFAULT_USERNAME
from .tasks import update_phylogenetic_tree
from cluster.util import *


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_tree(request):
    """

    This function is to update a tree
    request_params : title: String
    request_params : file_names : List (File names of DNA fna files)
    request_params : file_names : List (File names of kmer_forests)
    request_params : previous tree json object
    response : Matrix Generation Process details 

    """
    # process_id
    # file_name

    data = request.data
    data["username"] = str(request.user)

    tree_updation_request = PhylogeneticTreeUpdationRequest(data=data)

    if tree_updation_request.is_valid():
        tree_process = PhylogeneticTreeProcess.objects.get(
            id=request.data["process_id"])

        tree_creation = PhylogeneticTreeCreation.objects.get(
            process=tree_process)

        if tree_process.type == 1:

            updation_process = PhylogeneticTreeUpdate(
                process=tree_process, creation_process=tree_creation)

            updation_process.save()
            tree_process.type = 2

        else:
            updation_process = PhylogeneticTreeUpdate.objects.get(
                process=tree_process)

        if request.data["is_default_user"]:
            username = DEFAULT_USERNAME
        else:
            username = request.user

        directory = Directory.objects.get(name=username)

        dna_file = DNAFile.objects.get(
            file_name=request.data["file_name"], directory=directory)

        updation_process.dna_files.add(dna_file)
        updation_process.save()
        tree_process.status = 1

        tree_process.save()

        update_phylogenetic_tree.delay(
            process_id=tree_process.id, new_species_file_name=dna_file.object_key, defaultUser=request.data["is_default_user"])

        process_details = {
            "process_id": tree_process.id,
            "title": tree_process.title,
            "process_type": TreeProcessType.get_key(tree_process.type),
            "status": ProcessStatusTypes.get_key(tree_process.status),
            "method": ProcessTypes.get_key(tree_creation.type)
        }

        return Response({"process": process_details})

    else:
        return Response({"errors": tree_updation_request.errors})
