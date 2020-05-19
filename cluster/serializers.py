from rest_framework import serializers
from .models import *
from .util import *


class MatrixCreationProcessSerializer(serializers.Serializer):
    """ Vaidate the distance matrix creation request. """
    title = serializers.CharField(required=True)
    process_type = serializers.CharField(required=True)
    is_default_user = serializers.BooleanField(required=True)

    def validate_process_type(self, type):
        if type == "LSH" or type == "KMER":
            return type
        else:
            return serializers.ValidationError("This Process Type doesn't exist.")


class MatrixResultRequestSerializer(serializers.Serializer):

    """ Validate the distance matrix result request."""
    process_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=200)

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
        user = User.objects.get(username=attrs["username"])
        process = MatrixProcess.objects.filter(
            user=user, id=attrs["process_id"])
        process_tmp = MatrixProcess.objects.filter(id=attrs["process_id"])
        if process_tmp.exists():
            if not process.exists():
                raise serializers.ValidationError(
                    "You are not permitted to View the results.")

        return attrs


class TreeResultRequestSerializer(serializers.Serializer):

    """ Validate the Phylogenetic tree result request."""
    process_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=200)

    def validate_process_id(self, id):

        process = PhylogeneticTreeProcess.objects.filter(id=id)
        if not process.exists():
            raise serializers.ValidationError("This Process Doesn't exists!")
        else:
            process = process.first()
            if process.status == 1 and process.type == 1:
                raise serializers.ValidationError(
                    "Phylogenetric Tree creation is still in Progress")

    def validate(self, attrs):
        user = User.objects.get(username=attrs["username"])
        process = PhylogeneticTreeProcess.objects.filter(
            user=user, id=attrs["process_id"])
        process_tmp = PhylogeneticTreeProcess.objects.filter(
            id=attrs["process_id"])
        if process_tmp.exists():
            if not process.exists():
                raise serializers.ValidationError(
                    "You are not permitted to View the results.")

        return attrs


class TreeCreationRequestSerializer(serializers.Serializer):
    """ Validate the Phylogenetic Tree Creation Process Request."""
    title = serializers.CharField(required=True)
    matrix_process_id = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def validate_matrix_process_id(self, id):
        result = MatrixProcess.objects.filter(id=id)
        if not result.exists():
            raise serializers.ValidationError("This Result Doesn't exist!")
        return id

    def validate(self, attrs):
        user = User.objects.get(username=attrs["username"])
        process = MatrixProcess.objects.filter(
            user=user, id=attrs["matrix_process_id"])
        if not process.exists():
            raise serializers.ValidationError(
                "You don't have a matrix process with this id.")
        return attrs

    def validate_type(self, data):
        if data == "LSH" or data == "KMER":
            pass
        else:
            raise serializers.ValidationError(
                "This Process Type doesn't exist.")
