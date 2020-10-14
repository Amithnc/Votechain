from web3 import Web3
import json

ganache_url="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount=web3.eth.accounts[2]


abi=json.loads('[{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"}]')
address=web3.toChecksumAddress("0xA45742fDD28eF56c736033e53B9e567dF203F910")

contract=web3.eth.contract(address=address,abi=abi)
try:
  print(contract.functions.vote(1).transact())
except:
  print("you have already voted")

count=contract.functions.candidatesCount().call()
for i in range(1,count+1):
  party=(contract.functions.candidates(i).call())
  print(party)
# tx_hash=contract.functions.setGreeting('HELLO WORLD').transact()

# web3.eth.waitForTransactionReceipt(tx_hash)

# print("updated greeting {}".format(
#   contract.functions.greet().call()
#   ))