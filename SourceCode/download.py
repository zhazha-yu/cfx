# import the following dependencies
import json
from web3 import Web3
import asyncio
import time
import subprocess

# add your blockchain connection information

web3 = Web3(Web3.WebsocketProvider("ws://127.0.0.1:8546"))
print(web3.isConnected())
contract_address = '0x395F23CB07C72558f01E1e3F2a1E51a346d50441'
contract_abi = json.loads('[    {       "constant": false,      "inputs": [         {               "internalType": "string",               "name": "_name",                "type": "string"            },          {               "internalType": "string",               "name": "_hash",                "type": "string"            },          {               "internalType": "uint256",              "name": "_size",                "type": "uint256"           }       ],      "name": "addFile",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [         {               "internalType": "string",               "name": "_hash",                "type": "string"            }       ],      "name": "changeFile_hash",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [         {               "internalType": "string",               "name": "_name",                "type": "string"            }       ],      "name": "changeFile_name",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [         {               "internalType": "uint256",              "name": "_size",                "type": "uint256"           }       ],      "name": "changeFile_size",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [],       "name": "reset_count",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [],       "name": "sentInfo",     "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "anonymous": false,     "inputs": [         {               "indexed": false,               "internalType": "uint256",              "name": "count",                "type": "uint256"           }       ],      "name": "upload",       "type": "event" },  {       "constant": true,       "inputs": [],       "name": "get_count",        "outputs": [            {               "internalType": "uint256",              "name": "",             "type": "uint256"           }       ],      "payable": false,       "stateMutability": "view",      "type": "function"  },  {       "constant": true,       "inputs": [         {               "internalType": "uint256",              "name": "_index",               "type": "uint256"           }       ],      "name": "getFile_info",     "outputs": [            {               "internalType": "string",               "name": "",             "type": "string"            },          {               "internalType": "string",               "name": "",             "type": "string"            },          {               "internalType": "uint256",              "name": "",             "type": "uint256"           }       ],      "payable": false,       "stateMutability": "view",      "type": "function"  }]')
mycontract = web3.eth.contract(address=contract_address, abi=contract_abi)

account = web3.eth.accounts[0]
pw = '123456'

event_filter = mycontract.events.upload.createFilter(fromBlock='latest')
event_filter.get_new_entries()

def handle_event(event):
    _count=Web3.toJSON(event.args['count'])
    _count = int(_count)
    print(_count)
    #time.sleep(1)
    # #等待ipfs相应
    #subprocess.Popen('ipfs get -o ./download %s' % _hash, shell=True, stdout=subprocess.PIPE)
    #time.sleep(1)
    i = 0
    while i < _count :
        _hash = mycontract.functions.getFile_info(i).call()[1]#待修改
        print(_hash)
        time.sleep(1)
     #等待ipfs相应
        subprocess.Popen('ipfs get -o ./download %s' % _hash, shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        i = i+1 
    print("备份完成")

    # and whatever

# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)

# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = mycontract.events.upload.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

if __name__ == "__main__":
    main()