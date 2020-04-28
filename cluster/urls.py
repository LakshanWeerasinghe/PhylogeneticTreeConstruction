from django.urls import path
from .views import *

"""
    Urls pattens:

        1. BASE_URL/matrix/generate/ : Create a Distance Matrix generation Process
        2. BASE_URL/tree/generate/ : Create a Tree Generation Process
        3. BASE_URL/matrix/result/ : get the Distance Matrix
        4. BASE_URL/tree/result/ : get the Phylogenetric Tree
        5. BASE_URL/allProcesses/ : get all Processes generate by a user
       
"""

urlpatterns = [

    # 1
    path('matrix/generate/', generate_distance_matrix_view,
         name='matrix_generate'),

    # 2
    path('tree/generate/', phylogenetic_tree_generate_view,
         name='lsh_tree_generate'),

    # 3
    path('matrix/result/', get_process_matrix_result_view, name='matrix_result'),

    # 4
    path('tree/result/', get_process_tree_result_view, name='tree_result'),
    path("", test_view),

    # 5
    path('allProcesses/', get_user_processes_view, name="user_processes"),

    # 6
    path('matrix/generate/default/', generate_distance_matrix_using_default_files_view,
         name="matrix_generate_default")

]
