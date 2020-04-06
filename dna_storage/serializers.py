#models 
from .models import Directory, DNAFile

#django 
from django.contrib.auth.models import User

#rest framework
from rest_framework import serializers

class DirectorySerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, required=True)
    user = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user'])
        name = validated_data['username']

        direactory, created = Directory.objects.get_or_create(user=user, name=name)

        if created:
            direactory.save()
            return direactory

    class Meta:
        model = Directory
        fields = ('username', 'user')

class DNAFileSerializer(serializers.ModelSerializer):

    file_name = serializers.CharField(max_length=100)
    object_key = serializers.CharField(max_length=100)
    is_available = serializers.BooleanField(default=False)
    size = serializers.IntegerField(required=False)
    directory = serializers.CharField(max_length=100, required=True)


    # file already exist validation
    # file format validation
    def validate_object_key(self, object_key):
        
        if not "fna" == object_key.split('.')[-1]:
            raise serializers.ValidationError("Can only upload fastar files")

        dna_file = DNAFile.objects.filter(object_key=object_key)

        if dna_file.exists():
            raise serializers.ValidationError("This file already exisist")
            
        return object_key

    #spieces validation
    def validate_file_name(self, file_name):

        dna_file = DNAFile.objects.filter(file_name=file_name)
        if dna_file.exists():
            raise serializers.ValidationError("This spieces already exist")

        return file_name

    def create(self, validated_data):

        directory = Directory.objects.get(id=validated_data['directory'])
        is_available=False

        dna_file, created = DNAFile.objects.get_or_create(file_name=validated_data['file_name'], object_key=validated_data['object_key'],
                                                            is_available=is_available, size=2, directory=directory                                                            
                                                            )

        if created:
            dna_file.save()
            return dna_file

    class Meta:
        model = DNAFile
        fields = ("file_name", "object_key", "is_available", "size", "directory")

class DNAFileUploadedSerializer(serializers.Serializer):

    file_name = serializers.CharField(max_length=100, required=True)
    is_uploaded = serializers.IntegerField(required=True)

    #check file name exist
    def validate_file_name(self, file_name):

        dna_file = DNAFile.objects.filter(file_name=file_name)
        if not dna_file.exists():
            raise serializers.ValidationError("This Doesn't exist")
        return file_name

    # #validate the digit
    # def validate_is_uploaded(self, is_uploaded):

    #     print(is_uploaded)
    #     if is_uploaded == 0 :
    #         return is_uploaded
    #     else:
    #         raise serializers.ValidationError("In valid input")
        