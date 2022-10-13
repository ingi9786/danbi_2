"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

# from backend.config.settings import BASE_DIR
# ENV_FILE_PATH = BASE_DIR / '.env'

import pathlib
ENV_FILE_PATH = pathlib.Path(__file__).resolve().parent.parent / '.env'

dotenv.read_dotenv(str(ENV_FILE_PATH))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
