#models 
from .models import Directory, DNAFile

#rest framework
from rest_framework import serializers

class DirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = "__all__"


class DNAFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DNAFile
        fields = "__all__"