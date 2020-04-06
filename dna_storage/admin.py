from django.contrib import admin

from .models import DNAFile, Directory

# Register your models here.
admin.site.register(DNAFile)

admin.site.register(Directory)