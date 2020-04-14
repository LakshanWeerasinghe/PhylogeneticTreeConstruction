from django.urls import path
from .views import generate_distance_matrix_using_lsh_view

"""
    Urls pattens:

"""

urlpatterns = [

    path('lsh/', generate_distance_matrix_using_lsh_view, name='lsh'),

]
