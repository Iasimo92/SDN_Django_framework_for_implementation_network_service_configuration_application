from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from .models import Device
from netmiko import ConnectHandler
from napalm import get_network_driver
import sys
import os
from .forms import DeviceConfigForm
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
#from fabric import Connection
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

def index4(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Backup running config',
        
        'devices': devices
    }
    return render(request, 'index4.html', context)

def index5(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Backup running config',
        
        'devices': devices
    }
    return render(request, 'index5.html', context)

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

def get_running_config(request, device_id):
    # Get the Device object by its ID
    device = get_object_or_404(Device, pk=device_id)

    # Define the NAPALM driver and optional arguments
    driver = get_network_driver('ios')  # Assuming Cisco IOS
    optional_args = {'secret': device.secret}

    try:
        # Connect to the device using the regular password
        with driver(hostname=device.host, username=device.username, password=device.password, optional_args=optional_args) as device_conn:
            # Retrieve the running configuration
            running_config = device_conn.get_config('running')

        # Create the context with the device and running configuration
        context = {
            'device': device,
            'running_config': running_config,
        }

        # Render the running_config.html template with the context
        return render(request, 'running_config.html', context)

    except Exception as e:
        # Handle any exceptions that may occur during the connection or retrieval
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message)
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


def get_running_config(device):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=device.host, username=device.username, password=device.password)
        stdin, stdout, stderr = ssh_client.exec_command('show running-config')
        running_config = stdout.read().decode("utf-8")

        ssh_client.close()
        return running_config

    except paramiko.AuthenticationException:
        return "Authentication failed"
    except paramiko.SSHException as e:
        return f"SSH error: {e}"
    except Exception as e:
        return f"Error: {e}"

def show_running_config(request, device_id):
    try:
        device = Device.objects.get(id=device_id)
        
        netmiko_device = {
            'device_type': 'cisco_ios',
            'ip': device.host,
            'username': device.username,
            'password': device.password,
            'secret': device.secret,  # Assuming 'enable_password' is the secret for enable mode
        }

        with ConnectHandler(**netmiko_device) as ssh:
            ssh.enable()
            running_config = ssh.send_command("show running-config")

            if running_config:
                directory = 'configs'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                filename = os.path.join(directory, f"{device.name}_running_config.txt")

                with open(filename, 'w') as file:
                    file.write(running_config)
            else:
                return HttpResponse("Running configuration is empty", status=500)

        context = {
            'device': device,
            'running_config': running_config,
        }

        return HttpResponse(running_config)

    except Device.DoesNotExist:
        return HttpResponse("Device not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


def configure_ip(request):
    if request.method == 'POST':
        form = DeviceConfigForm(request.POST)
        if form.is_valid():
            hostname = form.cleaned_data['hostname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            interface = form.cleaned_data['interface']
            ip_address = form.cleaned_data['ip_address']
            subnet_mask = form.cleaned_data['subnet_mask']

            cisco_device = {
                'device_type': 'cisco_ios',
                'host': hostname,
                'username': username,
                'password': password,
                'secret': password,
            }

            try:
                net_connect = ConnectHandler(**cisco_device)
                net_connect.enable()

                commands = [
                    f"interface {interface}",
                    f"ip address {ip_address} {subnet_mask}",
                    "no shutdown",
                ]

                output = net_connect.send_config_set(commands)
                net_connect.disconnect()

                return HttpResponse(f"Device configured successfully. Output:\n{output}")

            except Exception as e:
                return HttpResponse(f"Error configuring device: {str(e)}")
    else:
        form = DeviceConfigForm()

    return render(request, 'device_config/configure_ip.html', {'form': form})