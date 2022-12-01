from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Device

def index(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Hello! You are using our test controller',
        
        'devices': devices
    }
    return render(request, 'base.html', context)


def device(request: HttpRequest,device_id)->HttpResponse:
    return HttpResponse(f'{device_id}')
 
# Create your views here.
