from django.urls import path
from .views import *


"""
    url patterns are :
        1. /getUrl/

"""

urlpatterns = [


    path('upload/', get_dna_sequence_upload_url_view, name='upload'),
    path('updateStatus/', dna_file_uploaded_view, name="updateStatus"),
    path('getFiles/', get_users_dna_file_details, name="usersFiles"),
    path('getDefaultFiles/', get_dna_bank_files, name="defaultFiles")
]
