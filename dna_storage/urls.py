from django.urls import path
<<<<<<< HEAD
from django.conf.urls import url
from .views import get_dna_sequence_upload_url_view, dna_file_uploaded_view
from . import views
=======
from .views import *
>>>>>>> c2e7188f07e30e02d8657cf1aa0d325a3b056f87

"""
    url patterns are :
        1. /getUrl/

"""

urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(),name='index'), 

    path('upload/', get_dna_sequence_upload_url_view, name='upload'),
    path('updateStatus/', dna_file_uploaded_view, name="updateStatus"),
    path('getFiles/', get_users_dna_file_details, name="usersFiles"),
]
