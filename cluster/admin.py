from django.contrib import admin

from .models import Process, Result, TreeResult

admin.site.register(Process)
admin.site.register(Result)
admin.site.register(TreeResult)
