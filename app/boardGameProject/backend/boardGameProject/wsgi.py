"""
WSGI config for boardGameProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
path = '/home/ubuntu/boardGameProject'
if path not in sys.path:
    sys.path.append('/home/ubuntu/boardGameProject')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boardGameProject.settings")

application = get_wsgi_application()
