from django.urls import path
from .views import get_dna_sequence_upload_url_view, dna_file_uploaded_view

"""
    url patterns are :
        1. /getUrl/

"""

urlpatterns = [
    path('upload/', get_dna_sequence_upload_url_view, name='upload'),
    path('updateStatus/', dna_file_uploaded_view, name="updateStatus")
]