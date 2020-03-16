"""
WSGI config for autocall project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/balpreet/aiautocall/aiautocall')

sys.path.append('/home/balpreet/aiautocall/./envn/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autocall.settings')

application = get_wsgi_application()
