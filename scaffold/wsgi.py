"""
WSGI config for scaffold project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from scaffold.boot import fix_path
fix_path()

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scaffold.settings")

from django.core.wsgi import get_wsgi_application
from djangae.wsgi import DjangaeApplication

application = DjangaeApplication(get_wsgi_application())
