from django.urls import path
from .views import *

"""
    Urls pattens:

        1. BASE_URL/cluster/matrix/generate/ : create distance matrix generation process.
        2. BASE_URL/cluster/tree/generate/ : create tree generation Process
        3. BASE_URL/cluster/matrix/result/ : get the distance Matrix
        4. BASE_URL/cluster/tree/result/ : get the phylogenetric Tree
        5. BASE_URL/cluster/allProcesses/ : get all processes generate by a user
        6. BASE_URL/cluster/matrix/generate/default/ : create diatance matrix process using default files.
       
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

    # 5
    path('allProcesses/', get_user_processes_view, name="user_processes"),

    # 6
    path('matrix/generate/default/', generate_distance_matrix_using_default_files_view,
         name="matrix_generate_default")

]
