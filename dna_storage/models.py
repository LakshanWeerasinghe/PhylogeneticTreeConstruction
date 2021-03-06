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
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)

    def get_file_details(self):
        return {
            "file_name": self.file_name,
            "object_key": self.object_key,
            "size": self.size
        }

    def __str__(self):
        return self.file_name


class KmerForest(models.Model):
    location = models.CharField(max_length=250)
    dna_file = models.ForeignKey(to=DNAFile, on_delete=models.CASCADE)
    kmer_count = models.IntegerField()
