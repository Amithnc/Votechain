from web3 import Web3
import json
import binascii

ganache_url="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))
abi=json.loads('[{"constant":false,"inputs":[{"name":"_party","type":"string"},{"name":"_name","type":"string"}],"name":"addCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"party","type":"string"},{"name":"candidate_name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"chairperson","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]')
checkcksum="0x753A92680AB7A7e7756804E6DBA91D39EE7C09f9"
address=web3.toChecksumAddress(checkcksum)
contract=web3.eth.contract(address=address,abi=abi)

def AddCandidate(party,name,account_id):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  try:
    hash=contract.functions.addCandidate(party,name).transact()
    add_transaction(hash)
    return "added"
  except EOFError as e :
    print(e)
    return "failed" 
    


def vote_candidate(id,account_id):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  status=contract.functions.voters(web3.eth.accounts[account_id]).call()
  if not status:
    try:
      contract.functions.vote(id).transact()
      return True
    except:
      return False
      
def result():    
  details=[]
  count=contract.functions.candidatesCount().call()
  for i in range(1,count+1):
    party=(contract.functions.candidates(i).call())
    details.append(party)
  return details  

def get_status(account_id):
  status=contract.functions.voters(web3.eth.accounts[account_id]).call()
  return status

def add_transaction(hash):
  transaction=web3.eth.getTransaction(hash)
  hexabyte_hash=str(binascii.hexlify(transaction.hash))
  print(hexabyte_hash[2:-1])
  print(transaction.input)  
  # message=contract.decode_function_input(transaction.input)
  # print(message)