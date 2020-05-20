from rest_framework import serializers
from cluster.models import *
from dna_storage.models import DNAFile
from app.settings import DEFAULT_USERNAME
from dna_storage.models import Directory, DNAFile


class PhylogeneticTreeUpdationRequest(serializers.Serializer):
    """ validate the tree updation request. """

    process_id = serializers.IntegerField(required=True)
    file_name = serializers.CharField(required=True)
    is_default_user = serializers.BooleanField(required=True)
    username = serializers.CharField(required=True)

    def validate_process_id(self, id):
        process = PhylogeneticTreeProcess.objects.filter(id=id)
        if not process.exists():
            raise serializers.ValidationError("This Process Doesn't exist.")
        else:
            process = process.first()
            creation_process = PhylogeneticTreeCreation.objects.get(
                process=process)
            if creation_process.type == 1:
                raise serializers.ValidationError("Can not update using LSH.")

    def validate(self, attrs):
        if attrs["is_default_user"]:
            username = DEFAULT_USERNAME
        else:
            username = attrs["username"]
        directory = Directory.objects.get(name=username)
        dna_file = DNAFile.objects.filter(
            directory=directory, file_name=attrs["file_name"], is_available=True)
        if not dna_file.exists():
            raise serializers.ValidationError("This file name doesn't exist.")
        return attrs
