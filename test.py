from web3 import Web3
import json

ganache_url="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount=web3.eth.accounts[0]


abi=json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
address=web3.toChecksumAddress("0xA28156d0932b346c6BdA91c19179513ed2d6BeC4")

contract=web3.eth.contract(address=address,abi=abi)
print(contract.functions.greet().call())

tx_hash=contract.functions.setGreeting('HELLO WORLD').transact()

web3.eth.waitForTransactionReceipt(tx_hash)

print("updated greeting {}".format(
  contract.functions.greet().call()
  ))