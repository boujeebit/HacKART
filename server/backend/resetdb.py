import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Imports
import contextlib, json

from core.settings import DATABASES
from django.contrib.auth.models import User

def resetDjangoDB():
    # Remove database file if exists
    with contextlib.suppress(FileNotFoundError):
        os.remove(DATABASES['default']['NAME'])
    
    # Remove migrations
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
    os.system('find . -path "*/migrations/*.pyc"  -delete')

    # Rebuild database
    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')   


def makeAdminUser():
    admin = User.objects.create_superuser("admin", "email@email.com", "password1")
    admin.save()

if __name__ == "__main__":
    resetDjangoDB()
    makeAdminUser()