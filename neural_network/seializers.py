from rest_framework import serializers
from cluster.models import *
from dna_storage.models import DNAFile


class PhylogeneticTreeUpdationRequest(serializers.Serializer):
    process_id = serializers.IntegerField(required=True)
    file_name = serializers.CharField(required=True)
    is_default_user = serializers.BooleanField(required=True)

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
