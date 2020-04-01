from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .services import FastarFileStorage
from django.conf import settings

class FastarFileUploadView(APIView):

    _response = dict()

    def post(self, request):

        print(settings.CUSTOM_STORAGE_OPTIONS)

        # dictionary of files recives from this request with 
        # speices name as the key and file as the value
        files = request.FILES

        #validate the recived files
        for speices_name, _file in files.items():
            if _file.name.split('.')[-1] != "fna":
                self._response["errors"] = "Invalid file extension for %s" %speices_name
                return Response(self._response, status=status.HTTP_400_BAD_REQUEST)
        
        #Save the files in file system
        #implemet dynamically change the directory name according to the user in /tmp folder
        file_storage = FastarFileStorage(settings.CUSTOM_STORAGE_OPTIONS)

        for speices_name, _file in files.items():
             #path save in the DB to be implemented
                #file name
                #extension
                #path
                #user

            #save the uploaded files in the /storage folder
             path = file_storage.save(_file.name, ContentFile(_file.read()))

        self._response["message"] = "Files Sucessfully uploaded"
        return Response(self._response, status=status.HTTP_200_OK)
             

