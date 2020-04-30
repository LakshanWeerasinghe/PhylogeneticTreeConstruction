from django.urls import path
from .views import generate_feature_extraction

"""
    url patterns are :
        

"""

urlpatterns = [
    path('features/', generate_feature_extraction, name='feature'),
]