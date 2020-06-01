# models
from .models import Directory, DNAFile

# django
from django.contrib.auth.models import User

# rest framework
from rest_framework import serializers


class DirectorySerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, required=True)
    user = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user'])
        name = validated_data['username']

        direactory, created = Directory.objects.get_or_create(
            user=user, name=name)

        if created:
            direactory.save()
            return direactory

    class Meta:
        model = Directory
        fields = ('username', 'user')


class DNAFileSerializer(serializers.ModelSerializer):
    """ Validate the Request of geting a Presigned URL. """

    file_name = serializers.CharField(max_length=100)
    object_key = serializers.CharField(max_length=100)
    is_available = serializers.BooleanField(default=False)
    size = serializers.IntegerField(required=False)
    directory = serializers.CharField(max_length=100, required=True)

    # file format validation
    def validate_object_key(self, object_key):

        if not "fna" == object_key.split('.')[-1]:
            raise serializers.ValidationError(
                "Can only upload fastar files with .fna Extension.")

        return object_key

    # validate if the file is already exist.
    # validate if the sepeies (file_name) is already exist.
    def validate(self, attrs):

        directory = Directory.objects.get(id=attrs['directory'])
        dna_files = DNAFile.objects.filter(
            directory=directory, object_key=attrs["object_key"], is_available=True)
        if dna_files.exists():
            raise serializers.ValidationError(
                "This file already in the Storage.")

        dnas = DNAFile.objects.filter(
            directory=directory, file_name=attrs["file_name"], is_available=True)
        if dnas.exists():
            raise serializers.ValidationError("This file name already exist.")
        return attrs

    # save the DNA file in db
    def create(self, validated_data):

        directory = Directory.objects.get(id=validated_data['directory'])
        is_available = False

        dna_file, created = DNAFile.objects.get_or_create(file_name=validated_data['file_name'], object_key=validated_data['object_key'],
                                                          is_available=is_available, size=validated_data[
                                                              'size'], directory=directory
                                                          )

        if created:
            dna_file.save()
            return dna_file

    class Meta:
        model = DNAFile
        fields = ("file_name", "object_key",
                  "is_available", "size", "directory")


class DNAFileUploadedSerializer(serializers.Serializer):
    """ Validate the Request of DNAFile upload status. """

    file_name = serializers.CharField(max_length=100, required=True)
    is_uploaded = serializers.BooleanField(required=True)
    directory = serializers.CharField(max_length=200, required=True)

    # check file name exist
    def validate(self, attrs):

        directory = Directory.objects.get(id=attrs['directory'])
        dna_file = DNAFile.objects.filter(
            directory=directory, file_name=attrs["file_name"])
        if dna_file.exists():
            return attrs
        else:
            raise serializers.ValidationError(
                "This File Doesn't Exist in the Storage.")
