from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from .models import Device
from netmiko import ConnectHandler
from napalm import get_network_driver
import sys

import xml.etree.ElementTree as ET
import json
import requests
from django.http import JsonResponse
from celery.result import AsyncResult
from django.contrib import messages
import subprocess
from .models import Device
from pysnmp.hlapi import *

NAPALM_MAPPINGS={
    'cisco_ios':'ios',
    'cisco_iosxe':'ios',
    
}

def firstPage(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')

def index(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Controller',
        
        'devices': devices
    }
    return render(request, 'base1.html', context)

def index2(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Statistics',
        
        'devices': devices
    }
    return render(request, 'index2.html', context)

def index3(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Interface Statistics',
        
        'devices': devices
    }
    return render(request, 'index3.html', context)

def get_device_stats(request: HttpRequest,device_id)->HttpResponse:
    device=Device.objects.get(pk=device_id)
    driver=get_network_driver(NAPALM_MAPPINGS[device.platform])
    optional_args1 = {'secret': 'ericsson'}
    with driver(device.host,device.username,device.password,optional_args=optional_args1) as device_conn:
        interfaces=device_conn.get_interfaces()
    context = {
            'device': device,
            'interfaces': interfaces,
        }
    print(interfaces)    
    return render(request, 'device.html', context)




def get_interfaces_counters(request, device_id):
    device = Device.objects.get(pk=device_id)
    driver = get_network_driver(NAPALM_MAPPINGS[device.platform])
    optional_args = {'secret': 'ericsson'}
    with driver(device.host, device.username, device.password, optional_args=optional_args) as device_conn:
        interfaces = device_conn.get_interfaces_counters()

    context = {
        'device': device,
        'device_stats': interfaces,
    }
    
    return render(request, 'device1_backup.html', context)

def get_interface_statistics(request: HttpRequest,device_id)->HttpResponse:
    devices=Device.objects.get(pk=device_id)
    driver=get_network_driver(NAPALM_MAPPINGS[devices.platform])
    optional_args1 = {'secret': 'ericsson'}
    with driver(devices.host,devices.username,devices.password,optional_args=optional_args1) as device_conn:
        interfaces1=device_conn.get_environment()
    context = {
            'device': devices,
            'interfaces': interfaces1,
        }
    
    
    print(interfaces1)
    #return HttpResponse(f'{interfaces1}')
    return render(request,'device1.html',context)


# Create your views here.
