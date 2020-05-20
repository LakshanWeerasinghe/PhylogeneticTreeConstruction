from django.contrib import admin

from .models import DNAFile, Directory, KmerForest

# Register your models here.
admin.site.register(DNAFile)
admin.site.register(Directory)
admin.site.register(KmerForest)
