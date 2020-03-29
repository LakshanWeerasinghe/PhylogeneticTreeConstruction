from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.contrib.auth.models import User

from .serializers import UserSerializer

# Create your views here.
class RegisterView(APIView):

    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request):

        new_user = request.data
        user_serializer = UserSerializer(data=new_user)

        if user_serializer.is_valid():
            user = User.objects.filter(username = new_user['username'])
            if not user.exists():
                user_serializer.save()
                return Response({ "data" : user_serializer.data }, status=HTTP_201_CREATED)
            else:
                return Response( { "errors" : "username already exists!" }, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"errors" : user_serializer.errors}, status=HTTP_400_BAD_REQUEST)


class AuthenticateView(APIView):

    #login
    def post(self, request):

        

