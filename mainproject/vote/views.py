from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
import json
from .utils import capture,train_model,recognize
import signal,os
def homepage(request):
    pid=capture()
    return HttpResponse("home")
def train(request):
    result=train_model()
    return HttpResponse("trained")

def recoginze_face(request):
    result=recognize()
    return HttpResponse("recognized")
