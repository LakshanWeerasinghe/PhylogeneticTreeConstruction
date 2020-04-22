from django.db import models
from django.contrib.auth.models import User


class Directory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DNAFile(models.Model):
    file_name = models.CharField(max_length=100)
    object_key = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)
    size = models.IntegerField(blank=True, null=True)
<<<<<<< HEAD
    directory = models.ForeignKey(Directory, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.file_name
=======
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)

    def get_file_details(self):
        return {
            "file_name": self.file_name,
            "object_key": self.object_key,
            "size": self.size
        }

    def __str__(self):
        return self.file_name
>>>>>>> c2e7188f07e30e02d8657cf1aa0d325a3b056f87
