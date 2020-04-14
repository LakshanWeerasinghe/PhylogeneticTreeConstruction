# dajnago
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# rest framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# models
from dna_storage.models import DNAFile, Directory
from .models import Process

# tasks
from .tasks import generate_distance_matrix_using_lsh_task


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

    # crate the process and stores in the database
    # django signals fires and generate celery task and
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

    return Response({"id": process.id}, status=HTTP_200_OK)
