from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Device

def index(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    context = {
        'title': 'Hello user of this network controller',
        'devices': devices
    }
    return render(request, 'base.html', context)


def get_devices(request: HttpRequest)->HttpResponse:
    pass
 
# Create your views here.
