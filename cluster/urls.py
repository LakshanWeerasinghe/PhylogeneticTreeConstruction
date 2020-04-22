from django.urls import path
from .views import *

"""
    Urls pattens:

        1. BASE_URL/lsh/matrix/generate/ : generate the distance matrix using LSH
        2. BASE_URL/lsh/tree/generate/ : generate tree using LSH KMedoid Clustering algorithm
        3. BASE_URL/matrix/result/ : get the Distance Matrix
        4. BASE_URL/tree/result/ : get the Phylogenetric Tree


"""

urlpatterns = [

    # 1
    path('lsh/matrix/generate/', generate_distance_matrix_using_lsh_view,
         name='lsh_matrix_generate'),

    # 2
    path('lsh/tree/generate/', generate_tree_using_lsh_view,
         name='lsh_tree_generate'),

    # 3
    path('matrix/result/', get_process_matrix_result_view, name='matrix_result'),

    # 4
    path('tree/result/', get_process_tree_result_view, name='tree_result'),
    path("", test_view),

    # 5
    path('allProcesses/', get_user_processes_view, name="user_processes")

]
