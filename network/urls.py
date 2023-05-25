"""SDN_Django_framework_for_implementation_network_service_configuration_application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
     path('', views.firstPage),
     path('manage/',views.index,name="manage"),
     path('manage2/',views.index2,name="manage2"),
     path('manage3/',views.index3,name="manage3"),
     path('device_statistics/<int:device_id>', views.get_interface_statistics,name="device_statistics"),
     path('interface_statistics/<int:device_id>', views.get_interfaces_counters, name="interface_statistics"),
     path('device/<int:device_id>', views.get_device_stats, name="device"),
     

     #path('devices', views.get_devices),
]
