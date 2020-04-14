#rest framework
from rest_framework.authtoken.models import Token

#users
from .serializers import UserSerializer

#dna storage
from dna_storage.models import Directory
from dna_storage.serializers import DirectorySerializer

def create_directory_for_user(user, username):

    """
    Save the directory in S3 storage per user

    :param user : User 
    :param username: string

    """
    user_id = getattr(user, 'id')

    data = {
            "username" : username,
            "user" : user_id
            }
    
    directory_serializer = DirectorySerializer(data=data)
    if directory_serializer.is_valid():
        directory_serializer.save()

def get_user_login_response(user):

    """
    Generate a dictonory of user details with username, first name, last name, email, token

    :param user : User
    :return response : Dictionary 

    """
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    response = serializer.data
    del response['password']
    response['token'] = token.key
    return response

