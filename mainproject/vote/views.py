from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from web3 import Web3
import json
from .utils import capture,train_model,recognize
import requests

def homepage(request):
    return render(request,'home.html')

def register(request):
    if request.method == "POST":
        aadhar=request.POST.get('aadhar',None)
        name=request.POST.get('name',None)
        email=request.POST.get('email',None)
        password=request.POST.get('password',None)
        phone=request.POST.get('phone',None)
        raw_url="http://127.0.0.1:7000/data/"
        url=raw_url+str(aadhar)
        response = requests.request("GET", url)
        temp=eval(response.text)
        if not temp:
            messages.warning(request, 'Aadhar card not found. Please check the aadhar number')
            return redirect('/register')
        data=temp[0]
        if data['name'].lower()!=name.lower():
            messages.warning(request, 'Name doest match with Aadhar database')
            return redirect('/register')
        if data['phone_number']!=phone:
            messages.warning(request, 'Phone Number doest match with aadhar database')
            return redirect('/register')
        if data['age']<18:
            messages.warning(request, 'sorry you cannot cast vote in this age')
            return redirect('/register')
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