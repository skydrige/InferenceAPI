"""
ASGI config for djangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import logging

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')


logging.basicConfig(level=logging.DEBUG)

application = get_asgi_application()
