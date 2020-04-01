from django.urls import path
from .views import FastarFileUploadView 

"""
    url patterns are :
        1. /file_system/upload/

"""

urlpatterns = [
    path('upload/', FastarFileUploadView.as_view(), name='upload'),
]