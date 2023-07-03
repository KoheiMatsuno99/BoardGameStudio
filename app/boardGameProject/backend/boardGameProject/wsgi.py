"""
WSGI config for boardGameProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('home/ubuntu/backend/boardGameProject')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.boardGameProject.backend.boardGameProject.settings")

application = get_wsgi_application()
