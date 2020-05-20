from django.urls import path
from .views import *

"""
    url patterns are :
        1. BASE_URL/dna_storage/upload/ : get preassigned url
        2. BASE_URL/dna_storage/updateStatus/ : update the uplaod status of dna file
        3. BASE_URL/dna_storage/getFiles/ : get details of dna files of a user
        4. BASE_URL/dna_storage/getDefaultFiles/ : get details of default dna files

"""

urlpatterns = [
    path('upload/', get_dna_sequence_upload_url_view, name='upload'),
    path('updateStatus/', dna_file_uploaded_view, name="updateStatus"),
    path('getFiles/', get_users_dna_file_details, name="usersFiles"),
    path('getDefaultFiles/', get_dna_bank_files, name="defaultFiles")
]
