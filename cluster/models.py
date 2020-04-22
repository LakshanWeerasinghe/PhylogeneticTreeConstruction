from .util import ProcessMethodTypes, ProcessType, StatusTypes
from django.db import models
from dna_storage.models import DNAFile
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Process(models.Model):
    title = models.CharField(max_length=200)
    type = models.IntegerField(choices=ProcessType.choises())
    method = models.IntegerField(choices=ProcessMethodTypes.choises())
    status = models.IntegerField(choices=StatusTypes.choises())
    crated_at = models.DateTimeField(auto_now_add=True)
    dna_files = models.ManyToManyField(to=DNAFile)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def get_process_details_as_dict(self):

        return {
            "title": self.title,
            "type":  ProcessType.get_key(self.type),
            "process_id": self.id,
            "method": ProcessMethodTypes.get_key(self.method),
            "status": StatusTypes.get_key(self.status)
        }

    def __str__(self):
        return self.title


class Result(models.Model):
    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)
    result = models.TextField()


class TreeResult(models.Model):
    process = models.ForeignKey(to=Process, on_delete=models.CASCADE)
    tree = JSONField()

    def __str__(self):
        return self.process.title
