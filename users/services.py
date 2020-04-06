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
