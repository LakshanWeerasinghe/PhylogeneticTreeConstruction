import os
import shutil


def create_directory(path):

    try:
        os.makedirs(path, exist_ok=True)
    except OSError as ex:
        print(ex)


def remove_directory(path):
    try:
        shutil.rmtree(path)
    except OSError as error:
        print("Error: %s - %s." % (error.filename, error.strerror))
        return "Folder Deleteing Faild"

    return True
