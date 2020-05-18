from rest_framework import serializers
from .models import *


class LSHDistanceMatrixSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.CharField())

    def validate_files(self, data):
        return data


class MatrixResultRequestSerializer(serializers.Serializer):

    """
    This Class is used to validate the Distance Matrix Result Viewing Request

    """
    process_id = serializers.IntegerField()
    username = serializers.CharField()

    def validate_process_id(self, id):

        process = MatrixProcess.objects.filter(id=id)
        if not process.exists():
            raise serializers.ValidationError("This Process Doesn't exists!")
        else:
            process = process.first()
        if process.status == 1:
            raise serializers.ValidationError(
                "Distance Matrix Generation is still in Progress")

    def validate(self, attrs):
        pass


class TreeResultRequestSerializer(serializers.Serializer):

    """
    This Class is used to validate the Phylogenetic Tree Result Viewing Request

    """
    process_id = serializers.IntegerField()

    def validate_process_id(self, id):

        process = PhylogeneticTreeProcess.objects.filter(id=id)
        if not process.exists():
            raise serializers.ValidationError("This Process Doesn't exists!")
        else:
            process = process.first()
        if process.status == 1:
            raise serializers.ValidationError(
                "Phylogenetric Tree creation is still in Progress")


class TreeCreationRequestSerializer(serializers.Serializer):
    """
    This class is used to validate the Phylogenetic Tree Creation Process Requests

    """
    title = serializers.CharField(required=True)
    matrix_process_id = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)

    # def validate_result_id(self, id):
    #     result = DNASimilaritiesResult.objects.filter(id=id)
    #     if not result.exists():
    #         raise serializers.ValidationError("This Result Doesn't exist!")
