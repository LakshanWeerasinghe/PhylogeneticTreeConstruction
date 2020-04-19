from django.urls import path
from django.conf.urls import url
from .views import get_dna_sequence_upload_url_view, dna_file_uploaded_view
from . import views

"""
    url patterns are :
        1. /getUrl/

"""

urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(),name='index'), 

    path('upload/', get_dna_sequence_upload_url_view, name='upload'),
    path('updateStatus/', dna_file_uploaded_view, name="updateStatus")
]