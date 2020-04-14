from rest_framework import serializers


class LSHDistanceMatrixSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.CharField())

    def validate_files(self, data):
        return data
