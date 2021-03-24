from django.shortcuts import render,redirect
from django.contrib import messages
from web3 import Web3
from .utils import capture,train_model,recognize
import requests
import random
from django.contrib.auth.decorators import login_required
from .models import voter_data
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth import get_user_model
from django.contrib import auth
# if request.user.is_authenticated():
from django.http import HttpResponse


def homepage(request):  
    # o=voter_data.objects.all()
    # print("last_object_id:-",o[len(o)-1].id)
    response_text={}
    if request.user.is_authenticated and not(request.user.is_superuser):
        usr=request.user
        aadhar=usr.aadhar_number
        raw_url="https://aadhar.pythonanywhere.com/data/"
        url=raw_url+str(aadhar)
        response = requests.request("GET", url)
        temp=eval(response.text)
        data=temp[0]
        response_text['name']=data['name']
        if not usr.is_verified:
            response_text['usr_id']=usr.id
    return render(request,'home.html',response_text)

otp=0

def register(request):
    if request.method == "POST":
        aadhar=request.POST.get('aadhar',None)
        name=request.POST.get('name',None)
        email=request.POST.get('email',None)
        password=request.POST.get('password',None)
        phone=request.POST.get('phone',None)
        user_input_otp=request.POST.get('otp',None)
        obj=voter_data.objects.filter(aadhar_number=aadhar)
        if len(obj)!=0:
            messages.warning(request, 'Already registered please use the key to vote')
            return redirect('/register')
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
        response_text={}
        response_text['message']="show"
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
                return render(request,'register.html',response_text)
            else:
                response_text['message']="show_last_info"
                obj=voter_data.objects.all()
                key_number=obj[len(obj)-1].key_number+1
                global passwd
                passwd=password
                response_text['url']=str(aadhar)+"&"+str(key_number)
                messages.success(request,'successfully verified your phone number')    
                return render(request,'register.html',response_text)
        return render(request,'register.html',response_text)
    return render(request,'register.html')

def generate_otp():
    number=""
    for _ in range(4):
        number+= str(random.randint(0,9))
    return int(number)


def capture_images(request,id):
    temp=id.split("&")
    voter_data.objects.create(
        aadhar_number=int(temp[0]),
        key_number=int(temp[1]),
        password=make_password(passwd),
        key="TEMP")
    obj=voter_data.objects.filter(aadhar_number=int(temp[0]))
    response=capture(obj[0].id)
    if response=="done":
        result=train()
        if result=="trained":
            #for getting key
            ganache_url="HTTP://127.0.0.1:7545"
            web3=Web3(Web3.HTTPProvider(ganache_url))
            ganache_key=web3.eth.accounts[int(temp[1])]
            voter_data.objects.filter(aadhar_number=int(temp[0])).update(key=ganache_key)
            raw_url="https://aadhar.pythonanywhere.com/data/"
            url=raw_url+temp[0]
            response = requests.request("GET", url)
            evaluated_response=eval(response.text)
            data=evaluated_response[0]
            phone=data['phone_number']
            # first_snippet="https://www.fast2sms.com/dev/bulkV2?authorization=ikvTwZbp4tSNDdmI1Ls8BjcFehOVAqglozuKQYMrUHaCn7R6G2atl7ZjPgYDkvNoMEueA32d6ws85O1C&route=v3&sender_id=TXTIND&message_text="
            # message="your%20KEY%20for%20Voting%20in%20VOTECHAIN%20is%20"+str(ganache_key)
            # next_snippet="&language=english&flash=0&numbers="+phone
            # url=first_snippet+message+next_snippet
            # requests.request("GET", url)
            messages.success(request,'Registration successful Key is sent to your mobile number')
            return redirect('/')   

def train():
    train_model()
    return "trained"

def login(request):
    response_text={}
    if request.method == "POST":
        key=request.POST.get('key',None)
        passwd=request.POST.get('password',None)
        user = auth.authenticate(key=key, password=passwd)
        if user:
            auth.login(request, user)
            if user.is_verified:
                messages.success(request,'successfully logged-in and your face-id is already verified so please continue to vote')
                return redirect("/")
            messages.success(request,'successfully logged-in please verify your face-id to continue to vote')
            return redirect("/")
        else:
            messages.warning(request,'WRONG CREDENTIALS PLEASE TRY AGAIN')
            response_text['message']="tab2"  
            return render(request,'register.html',response_text)

def logout(request):
    auth.logout(request)
    messages.success(request, 'logged-out successfully')
    return redirect("/")            

@login_required(login_url="/register")
def recoginze_face(request,id):
    response_text={}
    for i in range(5):    
        res=recognize()
        if res==int(id):
            break
    else:
        messages.warning(request,'unable to authorize your face-id please make sure u sit in well lighted area and try again')
        return redirect('/')
    voter_data.objects.filter(id=int(id)).update(is_verified=True)   
    messages.success(request,'successfully authenticated proceed to voting')
    return redirect('/')

