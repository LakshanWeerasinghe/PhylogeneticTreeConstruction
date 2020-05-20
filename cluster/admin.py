from django.contrib import admin

from .models import *

admin.site.register(MatrixProcess)
admin.site.register(DNASimilaritiesResult)
admin.site.register(PhylogeneticTreeProcess)
admin.site.register(PhylogeneticTreeCreation)
admin.site.register(PhylogeneticTreeResult)
