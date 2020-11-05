from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
import json
from .utils import capture
import signal,os
def homepage(request):
    pid=capture()
    os.kill(pid, signal.SIGTERM)
    return HttpResponse("home")