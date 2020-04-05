from django.urls import path
from .views import get_dna_sequence_upload_url

"""
    url patterns are :
        1. /getUrl/

"""

urlpatterns = [
    path('upload/', get_dna_sequence_upload_url, name='upload'),
]