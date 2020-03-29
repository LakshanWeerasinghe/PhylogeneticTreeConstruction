from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.contrib.auth.models import User

from .serializers import UserSerializer, RegisterSerializer

# Create your views here.
class RegisterView(APIView):

    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request):

        new_user = request.data
        register_serilalizer = RegisterSerializer(data=new_user)
        
        if register_serilalizer.is_valid():
            user_serializer = UserSerializer(data=new_user)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(user_serializer.data, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(register_serilalizer.errors, status=HTTP_400_BAD_REQUEST)

        

