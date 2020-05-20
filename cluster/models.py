from .util import *
from django.db import models
from dna_storage.models import DNAFile
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class MatrixProcess(models.Model):
    title = models.CharField(max_length=200)
    type = models.IntegerField(choices=ProcessTypes.choises())
    status = models.IntegerField(choices=ProcessStatusTypes.choises())
    crated_at = models.DateTimeField(auto_now_add=True)
    dna_files = models.ManyToManyField(to=DNAFile)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def get_process_details_as_dict(self):

        return {
            "process_id": self.id,
            "title": self.title,
            "type":  ProcessTypes.get_key(self.type),
            "status": ProcessStatusTypes.get_key(self.status)
        }

    def __str__(self):
        return self.title


class DNASimilaritiesResult(models.Model):
    process = models.ForeignKey(to=MatrixProcess, on_delete=models.CASCADE)
    result = models.TextField()

    def __str__(self):
        return self.process.title


class PhylogeneticTreeProcess(models.Model):
    title = models.CharField(max_length=200)
    type = models.IntegerField(choices=TreeProcessType.choises())
    status = models.IntegerField(choices=ProcessStatusTypes.choises())
    crated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def get_process_details_as_dict(self):

        return {
            "process_id": self.id,
            "title": self.title,
            "type":  TreeProcessType.get_key(self.type),
            "status": ProcessStatusTypes.get_key(self.status)
        }

    def __str__(self):
        return self.title


class PhylogeneticTreeResult(models.Model):
    process = models.ForeignKey(
        to=PhylogeneticTreeProcess, on_delete=models.CASCADE)
    tree = JSONField()

    def __str__(self):
        return self.process.title


class PhylogeneticTreeCreation(models.Model):
    type = models.IntegerField(choices=ProcessTypes.choises())
    process = models.ForeignKey(
        to=PhylogeneticTreeProcess, on_delete=models.CASCADE)
    matrix_process = models.ForeignKey(
        to=MatrixProcess, on_delete=models.CASCADE)
