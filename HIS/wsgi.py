"""
WSGI config for HIS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from os.path import join, dirname, abspath

PROJECT_DIR = dirname(dirname(abspath(__file__)))  # 3
sys.path.insert(0, PROJECT_DIR)  # 5
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HIS.settings')

application = get_wsgi_application()
