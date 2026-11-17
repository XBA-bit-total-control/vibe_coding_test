"""
ASGI config for todo_web_cite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_web_cite.settings')

django_application = get_asgi_application()

application = Starlette(routes=[
    Mount(settings.STATIC_URL.rstrip('/'), app=StaticFiles(directory=settings.STATIC_ROOT)),
    Mount('/', app=django_application),
])
