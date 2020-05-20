from django.db import models
from django.contrib.auth.models import User
from cluster.models import *
from dna_storage.models import DNAFile


class PhylogeneticTreeUpdate(models.Model):
    dna_files = models.ManyToManyField(to=DNAFile)
    creation_process = models.ForeignKey(
        to=PhylogeneticTreeCreation, on_delete=models.CASCADE)
    process = models.ForeignKey(
        to=PhylogeneticTreeProcess, on_delete=models.CASCADE)
