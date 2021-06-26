from django.shortcuts import render,redirect
from django.contrib import messages
from web3 import Web3
from .utils import capture,train_model,recognize
import requests
import random
from django.contrib.auth.decorators import login_required
from .models import voter_data,results_publish_status,transactions,parties
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth import get_user_model
from django.contrib import auth
# if request.user.is_authenticated():
from django.http import HttpResponse,JsonResponse
from .main_web3 import AddCandidate,vote_candidate,result,get_status,decrypt_hash,get_count

def homepage(request):
    # o=voter_data.objects.all()
    # print("last_object_id:-",o[len(o)-1].id)
    response_text={}
    usr=request.user
    results_obj=results_publish_status.objects.all()
    response_text['results_publish_status']=results_obj[0].Publish_result
    if request.user.is_authenticated and not(request.user.is_superuser):
        aadhar=usr.aadhar_number
        raw_url="https://aadhar.pythonanywhere.com/data/"
        url=raw_url+str(aadhar)
        response = requests.request("GET", url)
        temp=eval(response.text)
        data=temp[0]
        response_text['name']=data['name']
        response_text['aadhar_number']=aadhar
        response_text['age']=data['age']
        response_text['phone_number']=data['phone_number']
        response_text['image']="https://aadhar.pythonanywhere.com/"+data['image']
        if not usr.is_verified:
            response_text['usr_id']=usr.id
    if usr.is_authenticated:
        status=get_status(usr.key_number)
        if not status:
            response_text['vote']="TRUE"
        else:
            res_obj=results_publish_status.objects.all()
            if res_obj[0].Publish_result:
                response_text['results']="TRUE"
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
            messages.warning(request, ' You have already registered please use the key sent to your mobile number to vote')
            return redirect('/register')
        raw_url="https://aadhar.pythonanywhere.com/data/"
        url=raw_url+str(aadhar)
        response = requests.request("GET", url)
        temp=eval(response.text)
        if not temp:
            messages.error(request, 'Aadhar card/voter ID not found. Please check the aadhar/voter ID number')
            return redirect('/register')
        data=temp[0]
        if data['name'].lower()!=name.lower():
            messages.error(request, 'Name doesnt match with the database')
            return redirect('/register')
        if data['phone_number']!=phone:
            messages.error(request, 'Phone Number doesnt match with the database')
            return redirect('/register')
        if int(data['age'])<18:
            messages.error(request, 'sorry you cannot cast vote in this age')
            return redirect('/register')
        response_text={}
        response_text['message']="show"
        if user_input_otp=="" and password =="":
            global otp
            number=generate_otp()
            if len(str(number))!=4:
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
                messages.error(request, 'WRONG OTP PLEASE TRY AGAIN')
                return render(request,'register.html',response_text)
            else:
                response_text['message']="show_last_info"
                obj=voter_data.objects.all()
                if len(obj)==1:
                    key_number=0
                else:
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
        aadhar_number=temp[0],
        key_number=int(temp[1]),
        password=make_password(passwd),
        key="TEMP")
    obj=voter_data.objects.filter(aadhar_number=temp[0])
    response=capture(obj[0].id)
    if response=="done":
        result=train()
        if result=="trained":
            #for getting key
            ganache_url="HTTP://127.0.0.1:7545"
            web3=Web3(Web3.HTTPProvider(ganache_url))
            ganache_key=web3.eth.accounts[int(temp[1])]
            voter_data.objects.filter(aadhar_number=temp[0]).update(key=ganache_key)
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
                if request.user.is_superuser:
                    messages.success(request,'successfully logged-in')
                    return redirect("/")
                if get_status(user.key_number):
                    messages.success(request,'successfully logged-in and you have already voted so please check the results once it is out')
                    return redirect("/")
                messages.success(request,'successfully logged-in and your face-id is already verified so please continue to vote')
                return redirect("/")
            messages.success(request,'successfully logged-in please verify your face-id to continue to vote')
            return redirect("/")
        else:
            messages.error(request,'WRONG CREDENTIALS PLEASE TRY AGAIN')
            response_text['message']="tab2"
            return render(request,'register.html',response_text)

def logout(request):
    auth.logout(request)
    messages.success(request, 'logged-out successfully')
    return redirect("/")

@login_required(login_url="/register")
def recoginze_face(request,id):
    obj=voter_data.objects.filter(id=id)
    if len(obj)==0:
        messages.error(request,'NO FACE-ID FOUND WITH THE REQUESTED ID')
        return redirect('/')
    for i in range(5):
        res=recognize()
        if res==int(id):
            break
    else:
        messages.error(request,'unable to authorize your face-id please make sure you sit in well lighted area and try again')
        return redirect('/')
    voter_data.objects.filter(id=int(id)).update(is_verified=True)
    messages.success(request,'successfully authenticated proceed to voting')
    return redirect('/')

@login_required(login_url="/register")
def addCandidate(request):
    if not request.user.is_superuser:
        messages.error(request,'You have to be admin to add candidates')
        return redirect("/")
    usr=request.user
    if request.method == "POST":
        party=request.POST.get('party',None)
        candidate_name=request.POST.get('candidate_name',None)
        symbol_file=request.FILES['symbol_file']
        res=AddCandidate(party,candidate_name,usr.key_number)
        if res:
            parties_obj=parties.objects.all()
            if len(parties_obj)==0 or parties_obj[len(parties_obj)-1].checksum  ==res :
                parties.objects.create(checksum=res,candidate_id=get_count(),symbol=symbol_file)
            else:
                for obj in parties_obj:
                    obj.delete() 
                parties.objects.create(checksum=res,candidate_id=get_count(),symbol=symbol_file)   
            messages.success(request,'Candidate Added Successfully')
            return redirect("/")
        else:
            messages.error(request,'Some error occured during the process please try again later')
            return redirect("/")

@login_required(login_url="/register")
def cast_vote(request):
    response_text={}
    usr=request.user
    if not usr.is_verified:
        messages.error(request,'please verify your face-id frist and then proceed with this step')
        return redirect('/')
    if get_status(usr.key_number):
        messages.error(request,'You have already voted')
        return redirect('/')
    if request.method == "POST":
        candidate_id=request.POST.get('candidate_id',None)
        if vote_candidate(int(candidate_id),usr.key_number):
            messages.success(request,'Successfully voted check the results when it is out')
            return JsonResponse({'meassage':'success'})
        else:
            messages.error(request,'some error occured during voting please try after sometime')
            return redirect('/')
    details=result()
    party=[]
    candidates=[]
    symbol=[]
    party_and_candidates_number=[]
    for i in range(len(details)):
        party.append(details[i][1])
        candidates.append(details[i][2])
        symbol_obj=parties.objects.filter(candidate_id=details[i][0])
        symbol.append(symbol_obj[0])
        party_and_candidates_number.append(details[i][0])  
    response_text['details']=zip(party_and_candidates_number,party,candidates,symbol)
    return render(request,'vote.html',response_text)


@login_required(login_url="/register")
def publish_result(request):
    if not request.user.is_superuser:
        messages.error(request,'You have to be admin to publish results')
        return redirect("/")
    status_obj=results_publish_status.objects.all()
    if status_obj[0].Publish_result :
        results_publish_status.objects.filter(id=status_obj[0].id).update(Publish_result=False)
    else:
        results_publish_status.objects.filter(id=status_obj[0].id).update(Publish_result=True)
    if status_obj[0].Publish_result:
        messages.success(request,'Successfully Published the results')
    else:
        messages.success(request,'Successfully withholded the results')
    return redirect("/")
@login_required(login_url="/register")
def results(request):
    usr=request.user
    response_text={}
    results_obj=results_publish_status.objects.all()
    if not results_obj[0].Publish_result:
        messages.error(request,'Results are not yet published')
        return redirect('/')
    if get_status(usr.key_number):
        details=result()
        party_and_candidates=[]
        party=[];candidate=[]
        final_results=[]
        results=[]
        colors=[]
        d={}
        for i in range(len(details)):
            party_and_candidates.append((details[i][1])+" - "+(details[i][2]))
            d[(details[i][1])+" - "+(details[i][2])]=details[i][3]
            final_results.append(details[i][3])
            temp='rgb({},{},{})'.format(random.randint(0,226),random.randint(0,226),random.randint(0,226))
            colors.append(temp)
        d=dict(sorted(d.items(),key=lambda item:item[1],reverse=True))
        for key,value in d.items():
            temp=key.split("-")
            party.append(temp[0]);candidate.append(temp[1]);results.append(value)
        response_text['details']=party_and_candidates
        response_text['results']=final_results
        response_text['colors']=colors
        response_text['mainlist']=zip(party,candidate,results)
        response_text['d']=d
        return render(request,'result.html',response_text)
    else:
        messages.error(request,'You have to vote first to see the results')
        return redirect("/")

def get_blocks_details(request):
    #decrypt the hash
    if request.method == "POST":
        hash=request.POST.get('hash',None)
        if hash != '-':
            obj=transactions.objects.filter(hash_value=hash)
            obj=obj[0]
            if obj.catagory=='vote':
                decrypted_value=str(decrypt_hash(obj.input_value,catagory="vote"))
            else:
                decrypted_value=str(decrypt_hash(obj.input_value))
            return JsonResponse({"result": decrypted_value}, status=200)
        else:
            return JsonResponse({"result": "No data present as it is a contract creation block"}, status=200)


    transactions_obj=transactions.objects.all()
    return_response={'transactions':transactions_obj}
    return render(request,'block_details.html',return_response)

