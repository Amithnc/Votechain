from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
import json
from .utils import capture,train_model,recognize
import requests

def homepage(request):
    return render(request,'home.html')

def register(request):
    return render(request,'register.html')

def capture_images(request):
    pid=capture()
    return HttpResponse("home")

def train(request):
    result=train_model()
    return HttpResponse("trained")

def recoginze_face(request):
    while True:    
        res=recognize()
        if res==True:
            break
    print(res)
    return HttpResponse("recognized")

def api(request):
    url="http://127.0.0.1:7000/data/301539499355"
    response = requests.request("GET", url)
    y=eval(response.text)
    s=y[0]
    print(s['aadhar_number'])
    # y=json.loads(str(response))
    # print(y)
    return HttpResponse(response)