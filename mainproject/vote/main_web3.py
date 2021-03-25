from web3 import Web3
import json

ganache_url="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))
abi=json.loads('[{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"chairperson","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"}],"name":"addCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"}]')
address=web3.toChecksumAddress("0xC68Ee9e3F90fb21Fd87a4eC7A9Eb4AFAa7B17E1F")
contract=web3.eth.contract(address=address,abi=abi)

def AddCandidate(name,account_id):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  try:
    contract.functions.addCandidate(name).transact()
    return "added"
  except:
    return "failed"  


def vote(id,account_id,address):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  status=contract.functions.status(address).call()
  if status:
    try:
      contract.functions.vote(id).transact()
    except:
      print("already voted")
      
def result():    
  count=contract.functions.candidatesCount().call()
  print(count)
  for i in range(1,count+1):
    party=(contract.functions.candidates(i).call())
    print(party)
      

