from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello stream</h1>")
# Create your views here.
