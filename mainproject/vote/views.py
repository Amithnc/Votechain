from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from web3 import Web3
import json
from .utils import capture,train_model,recognize
import requests
import random

def homepage(request):
    return render(request,'home.html')
otp=0
def register(request):
    if request.method == "POST":
        aadhar=request.POST.get('aadhar',None)
        name=request.POST.get('name',None)
        email=request.POST.get('email',None)
        password=request.POST.get('password',None)
        phone=request.POST.get('phone',None)
        user_input_otp=request.POST.get('otp',None)
        raw_url="https://aadhar.pythonanywhere.com/data/"
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
        if int(data['age'])<18:
            messages.warning(request, 'sorry you cannot cast vote in this age')
            return redirect('/register')
        response_test={}
        response_test['message']="show"
        if user_input_otp=="" and password =="":
            global otp
            number=generate_otp()
            otp=number
            print(otp,"otp----when sending")
            # first_snippet="https://www.fast2sms.com/dev/bulkV2?authorization=ikvTwZbp4tSNDdmI1Ls8BjcFehOVAqglozuKQYMrUHaCn7R6G2atl7ZjPgYDkvNoMEueA32d6ws85O1C&route=v3&sender_id=TXTIND&message_text="
            # message="your%20OTP%20for%20registration%20to%20VOTECHAIN%20is%20"+str(otp)
            # next_snippet="&language=english&flash=0&numbers="+phone
            # url=first_snippet+message+next_snippet
            # requests.request("GET", url)
            messages.success(request, 'OTP sent to your phone number')
        else:
            # print(otp,"otp----in check")
            if otp!=int(user_input_otp):
                messages.warning(request, 'WRONG OTP PLEASE TRY AGAIN')
                return render(request,'register.html',response_test)
            else:
                response_test['message']="show_last_info"
                response_test['user_id']="amith_n_c"
                messages.success(request,'successfully verified your phone number')    
                return render(request,'register.html',response_test)
        return render(request,'register.html',response_test)
    return render(request,'register.html')

def generate_otp():
    number=""
    for _ in range(4):
        number+= str(random.randint(0,9))
    return int(number)


def capture_images(request,id):
    response=capture(id)
    if response=="done":
        result=train()
        if result=="trained":
            messages.success(request,'Registration Successfull Key is sent to your mobile number')
            return redirect('/')   

def train():
    train_model()
    return "trained"

def recoginze_face(request):
    while True:    
        res=recognize()
        if res==True:
            break
    print(res)
    return HttpResponse("recognized")

