from django.contrib import admin

from .models import *
admin.site.register(Process)
admin.site.register(Result)
admin.site.register(TreeResult)


admin.site.register(MatrixProcess)
admin.site.register(DNASimilaritiesResult)
admin.site.register(KMerForestResult)
admin.site.register(PhylogeneticTreeProcess)
admin.site.register(PhylogeneticTreeResult)
