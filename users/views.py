#django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

#rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

#other
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .services import create_directory_for_user, get_user_login_response

@api_view(["POST"])
def registration_view(request):
    new_user = request.data
    register_serilalizer = RegisterSerializer(data=new_user)

    #validate the payload of the request
    if register_serilalizer.is_valid():
        user_serializer = UserSerializer(data=new_user)
        if user_serializer.is_valid():

            user = user_serializer.save()

            #save the diractory name for the user
            create_directory_for_user(user, new_user['username'])

            response = get_user_login_response(user)
            return Response(response, status=HTTP_201_CREATED)
        else:
            return Response(user_serializer.data, status=HTTP_400_BAD_REQUEST)
    else:
        return Response(register_serilalizer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):

    login_serializer = LoginSerializer(data=request.data)
    if login_serializer.is_valid():
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            response = get_user_login_response(user)
            return Response(response, status=HTTP_200_OK)
        else:
            return Response({"error" : "wrong credentials"}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response(login_serializer.errors, status=HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    response = {
        "message" : "Successfully Loggedout"
    }
    return Response(response, status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_details_view(request):
    return Response()

class HomeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("Authentication Suceessfull")


