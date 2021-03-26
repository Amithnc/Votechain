from web3 import Web3
import json

ganache_url="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))
abi=json.loads('[{"constant":false,"inputs":[{"name":"_party","type":"string"},{"name":"_name","type":"string"}],"name":"addCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"party","type":"string"},{"name":"candidate_name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"chairperson","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]')
address=web3.toChecksumAddress("0x923fC114Eb1bF58f140E2731E889903441bF2e57")
contract=web3.eth.contract(address=address,abi=abi)

def AddCandidate(party,name,account_id):
  web3.eth.defaultAccount=web3.eth.accounts[account_id]
  try:
    contract.functions.addCandidate(party,name).transact()
    return "added"
  except:
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