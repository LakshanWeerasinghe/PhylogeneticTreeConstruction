#django
from django.urls import path

#view functions
from .views import registration_view, login_view, logout_view, HomeView

"""
    url patterns are :
        1. BASE_URL/users/register/  
        2. BASE_URL/users/login/
        3. BASE_URL/users/logout/

"""

urlpatterns = [

    #register new user
    path('register/', registration_view, name='register'),

    #login a registered user
    path('login/', login_view, name="login"),

    #logged out registed user
    path('logout/', logout_view, name="logout"),

    path('home/', HomeView.as_view(), name="home"),

]