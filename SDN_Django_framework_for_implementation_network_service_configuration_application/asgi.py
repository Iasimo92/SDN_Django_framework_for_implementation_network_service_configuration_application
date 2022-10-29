"""
ASGI config for SDN_Django_framework_for_implementation_network_service_configuration_application project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SDN_Django_framework_for_implementation_network_service_configuration_application.settings')

application = get_asgi_application()
