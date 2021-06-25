from web3 import Web3
import json
import binascii
from .models import transactions


ganache_url="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))
abi=json.loads('[{"constant":false,"inputs":[{"name":"_party","type":"string"},{"name":"_name","type":"string"}],"name":"addCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"party","type":"string"},{"name":"candidate_name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"chairperson","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]')
checksum="0xCDcf396043CFDA9a799ceaE57Fb2BF703a09C629"
address=web3.toChecksumAddress(checksum)
contract=web3.eth.contract(address=address,abi=abi)

def AddCandidate(party,name,account_id):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  try:
    hash=contract.functions.addCandidate(party,name).transact()
    add_transaction(hash,'add_candidate')
    return checksum
  except Exception as e :
    print(e)
    return False 
    

def vote_candidate(id,account_id):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  status=contract.functions.voters(web3.eth.accounts[account_id]).call()
  if not status:
    try:
      hash=contract.functions.vote(id).transact()
      add_transaction(hash,'vote')
      return True
    except Exception as e :
      print(e)
      return False
      
def result():    
  details=[]
  count=contract.functions.candidatesCount().call()
  for i in range(1,count+1):
    party=(contract.functions.candidates(i).call())
    details.append(party)  
  return details  

def get_count():
  count=contract.functions.candidatesCount().call()
  return count

def get_status(account_id):
  status=contract.functions.voters(web3.eth.accounts[account_id]).call()
  return status

def add_transaction(hash,type):
  transactions_obj=transactions.objects.all()
  transaction=web3.eth.getTransaction(hash)
  hexabyte_hash=str(binascii.hexlify(transaction.hash))
  hash=hexabyte_hash[2:-1]
  input_value=transaction.input
  if len(transactions_obj) == 0:
    transactions.objects.create(catagory="contract_creation",checksum=checksum,node_id=0)
    latest_obj=transactions.objects.latest('id')
    transactions.objects.create(hash_value=hash,catagory=type,checksum=checksum,input_value=input_value,pid=latest_obj.node_id,node_id=latest_obj.node_id+1)
  else:
    if (transactions_obj[len(transactions_obj)-1].checksum)  == checksum:
      latest_obj=transactions.objects.latest('id')
      transactions.objects.create(hash_value=hash,catagory=type,checksum=checksum,input_value=input_value,pid=latest_obj.node_id,node_id=latest_obj.node_id+1)
    else:
      for obj in transactions_obj:
        obj.delete()
      transactions.objects.create(catagory="contract_creation",checksum=checksum,node_id=0)
      latest_obj=transactions.objects.latest('id')
      transactions.objects.create(hash_value=hash,catagory=type,checksum=checksum,input_value=input_value,pid=latest_obj.node_id,node_id=latest_obj.node_id+1)  
  # message=contract.decode_function_input(transaction.input)
  # print(message)
def decrypt_hash(input_value,catagory=False):
  message=contract.decode_function_input(input_value)
  if catagory:
    candidateId=message[1]['_candidateId']
    party=(contract.functions.candidates(candidateId).call())
    message={'_candidateId':party[0],'_party':party[1],'_candidatename':party[2]}
  return message