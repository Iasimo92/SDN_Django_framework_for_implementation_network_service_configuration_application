from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from .models import Device
from netmiko import ConnectHandler
from napalm import get_network_driver
import sys
import paramiko
import xml.etree.ElementTree as ET
import json
import requests
from django.http import JsonResponse
from celery.result import AsyncResult
from django.contrib import messages
import subprocess
from .models import Device
from pysnmp.hlapi import *
from fabric import Connection
import logging
import subprocess

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


def execute_script_on_remote(request):
    if request.method == 'POST':
        remote_host = request.POST.get("remote_host")
        remote_user = request.POST.get("remote_user")
        remote_password = request.POST.get("remote_password")
        remote_script_path = request.POST.get("remote_script_path")

        try:
            # Establish SSH connection to the remote machine
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(remote_host, username=remote_user, password=remote_password)

            # Execute the script remotely with sudo
            command = f'sudo -S bash {remote_script_path}'
            stdin, stdout, stderr = ssh_client.exec_command(command)
            stdin.write(remote_password + '\n')
            stdin.flush()

            # Optionally, you can wait for the command to finish and get the output
            exit_status = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            ssh_client.close()

            if exit_status != 0:
                # Handle error case
                return JsonResponse({'status': 'error', 'message': f"Error executing the script: {error}"})
            else:
                # Process the output if needed
                return JsonResponse({'status': 'success', 'message': "Script executed successfully", 'output': output})

        except Exception as e:
            # Handle exceptions
            return JsonResponse({'status': 'error', 'message': f"Error connecting to the remote machine: {str(e)}"})

    else:
        # Return an error response for invalid request method (GET)
        return JsonResponse({'status': 'error', 'message': 'Invalid request method. Use POST method for script execution.'})