"""
WSGI config for SDN_Django_framework_for_implementation_network_service_configuration_application project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SDN_Django_framework_for_implementation_network_service_configuration_application.settings')

application = get_wsgi_application()
