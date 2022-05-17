from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

# Create your views here.

def index(request):
    return HttpResponse('Hello, world')

def home(request):
    # return HttpResponse('Hello, world')
    response = requests.get('https://www.getpostman.com/collections/8e31aea5ee9eeb38f8af')
    data = response.json()

    print(data)


    # print(data["item"][1])

    return render(request, 'superuser/layout.html', {'data': data})

