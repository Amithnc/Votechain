from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
import json

# Create your views here.
    ganache_url="HTTP://127.0.0.1:7545"
    web3=Web3(Web3.HTTPProvider(ganache_url))

    return HttpResponse('Homepage')