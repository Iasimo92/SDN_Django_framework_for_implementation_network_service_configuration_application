from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Device
from netmiko import ConnectHandler
from napalm import get_network_driver

NAPALM_MAPPINGS={
    'cisco_ios':'ios',
    'cisco_iosxe':'ios',
    
}

def index(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Hello! You are using our test controller',
        
        'devices': devices
    }
    return render(request, 'base.html', context)


def get_device_stats(request: HttpRequest,device_id)->HttpResponse:
    device=Device.objects.get(pk=device_id)
    driver=get_network_driver(NAPALM_MAPPINGS[device.platform])
    optional_args1 = {'secret': 'ericsson'}
    with driver(device.host,device.username,device.password,optional_args=optional_args1) as device_conn:
        interfaces=device_conn.get_interfaces()
    print(interfaces)    
    return HttpResponse(f'{device_id}')
 
# Create your views here.
