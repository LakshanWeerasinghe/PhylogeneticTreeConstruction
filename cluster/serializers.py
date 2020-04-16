from rest_framework import serializers
from .models import Process


class LSHDistanceMatrixSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.CharField())

    def validate_files(self, data):
        return data


class MatrixResultRequestSerializer(serializers.Serializer):
    process_id = serializers.IntegerField()

    def validate_process_id(self, id):

        process = Process.objects.filter(id=id)
        if not process.exists():
            raise serializers.ValidationError("This Process Doesn't exists!")
        else:
            process = process.first()
        if process.status == 1:
            raise serializers.ValidationError(
                "This Process is still in Progress")
        if process.type == 2:
            raise serializers.ValidationError(
                "Result cannot be obtained from this process type")


class TreeResultRequestSerializer(serializers.Serializer):
    process_id = serializers.IntegerField()

    def validate_process_id(self, id):

        process = Process.objects.filter(id=id)
        if not process.exists():
            raise serializers.ValidationError("This Process Doesn't exists!")
        else:
            process = process.first()
        if process.status == 1:
            raise serializers.ValidationError(
                "This Process is still in Progress")
        if process.type == 1:
            raise serializers.ValidationError(
                "Result cannot be obtained from this process type")
