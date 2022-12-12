from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from .models import Device
from netmiko import ConnectHandler
from napalm import get_network_driver



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
    return render(request, 'base.html', context)

def index2(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Statistics',
        
        'devices': devices
    }
    return render(request, 'index2.html', context)



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
   
def get_interface_statistics(request: HttpRequest,device_id)->HttpResponse:
    device=Device.objects.get(pk=device_id)
    driver=get_network_driver(NAPALM_MAPPINGS[device.platform])
    optional_args1 = {'secret': 'ericsson'}
    commands=['show interfaces summary']
    with driver(device.host,device.username,device.password,optional_args=optional_args1) as device_conn:
        statistics=device.cli(commands)
    context = {
            'device': device,
            'interfaces': statistics,
        }
    print(statistics)    
    return render(request, 'base1.html', context)
               
 
# Create your views here.
