from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
import json
from .utils import capture,train_model,recognize
#need not stop the thread of cv2 
def homepage(request):
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
