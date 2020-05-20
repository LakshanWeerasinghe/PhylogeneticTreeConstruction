from django.urls import path
from .views import update_tree

"""
    url patterns are :
        

"""

urlpatterns = [
    path('update_tree/', update_tree, name='update'),
]