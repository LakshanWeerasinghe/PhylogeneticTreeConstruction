from django.core.files.storage import FileSystemStorage
from django.conf import settings


class FastarFileStorage(FileSystemStorage):

    def _save(self, name, content):
        return super()._save(name, content)
