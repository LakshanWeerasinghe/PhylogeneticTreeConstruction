from django.db import models
from django.contrib.auth.models import User

class Directory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class DNAFile(models.Model):
    file_name = models.CharField(max_length=100, unique=True)
    object_key = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=False)
    size = models.IntegerField(blank=True, null=True)
    directory = models.ForeignKey(Directory, on_delete=models.DO_NOTHING)