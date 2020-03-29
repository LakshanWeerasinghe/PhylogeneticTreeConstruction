#django 
from django.contrib.auth.models import User

#django rest_framework 
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#other
import re

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name =  serializers.CharField()
    last_name =  serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        user, created = User.objects.get_or_create(username=validated_data['username'], email=validated_data['email'],
                                                    first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        if created:
            user.set_password(validated_data['password'])
            user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        write_only_fields = ('username',)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password =  serializers.CharField(required=True)
    confirm_password =  serializers.CharField(required=True)

    def validate_email(self, email):
        user = User.objects.filter(email = email)
        if user.exists():
            raise serializers.ValidationError("email already exists!")
        return email

    def validate_username(self,username):
        user = User.objects.filter(username = username)
        if user.exists():
            raise serializers.ValidationError("username already exists!")
        return username
    
    # def validate_password(self, password):
    #     if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
    #         raise serializers.ValidationError("User password should have minimum 8 characters")

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords doesn't match")
        return data
