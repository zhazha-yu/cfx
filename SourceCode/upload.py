# -*— codeing = utf-8 -*-
# 本照片意在将指定目录及其子目录中的照片读取，并将照片数据传入json照片中
import os
import json
import subprocess

import time
from web3 import Web3,HTTPProvider

web3 = Web3(Web3.WebsocketProvider("ws://127.0.0.1:8546"))
print(web3.isConnected())
contract_address = '0x395F23CB07C72558f01E1e3F2a1E51a346d50441'
contract_abi = json.loads('[    {       "constant": false,      "inputs": [         {               "internalType": "string",               "name": "_name",                "type": "string"            },          {               "internalType": "string",               "name": "_hash",                "type": "string"            },          {               "internalType": "uint256",              "name": "_size",                "type": "uint256"           }       ],      "name": "addFile",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [         {               "internalType": "string",               "name": "_hash",                "type": "string"            }       ],      "name": "changeFile_hash",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [         {               "internalType": "string",               "name": "_name",                "type": "string"            }       ],      "name": "changeFile_name",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [         {               "internalType": "uint256",              "name": "_size",                "type": "uint256"           }       ],      "name": "changeFile_size",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [],       "name": "reset_count",      "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "constant": false,      "inputs": [],       "name": "sentInfo",     "outputs": [],      "payable": false,       "stateMutability": "nonpayable",        "type": "function"  },  {       "anonymous": false,     "inputs": [         {               "indexed": false,               "internalType": "uint256",              "name": "count",                "type": "uint256"           }       ],      "name": "upload",       "type": "event" },  {       "constant": true,       "inputs": [],       "name": "get_count",        "outputs": [            {               "internalType": "uint256",              "name": "",             "type": "uint256"           }       ],      "payable": false,       "stateMutability": "view",      "type": "function"  },  {       "constant": true,       "inputs": [         {               "internalType": "uint256",              "name": "_index",               "type": "uint256"           }       ],      "name": "getFile_info",     "outputs": [            {               "internalType": "string",               "name": "",             "type": "string"            },          {               "internalType": "string",               "name": "",             "type": "string"            },          {               "internalType": "uint256",              "name": "",             "type": "uint256"           }       ],      "payable": false,       "stateMutability": "view",      "type": "function"  }]')
mycontract = web3.eth.contract(address=contract_address, abi=contract_abi)

account = web3.eth.accounts[0]
pw = '123456'


file = {}
def unlockAccount():
    #解锁账户
    web3.geth.personal.unlock_account(account, pw)

def reset():
    #更新合约中count为将待备份文件的个数
    tx_hash = mycontract.functions.reset_count().transact({'from': web3.eth.accounts[0],'to':contract_address,'gas': 4200000, 'gasPrice': 0x630000000})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    time.sleep(5)
def sentInfo():
    #hash上链完成并触发合约中的事件，以便备份服务器监听
    tx_hash = mycontract.functions.sentInfo().transact({'from': web3.eth.accounts[0],'to':contract_address,'gas': 4200000, 'gasPrice': 0x630000000})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)


def onchain(_hash,_name,_size):
    #将得到hash后的文件信息上链
    tx_hash = mycontract.functions.addFile(_name,_hash,_size).transact({'from': web3.eth.accounts[0],'to':contract_address,'gas': 4200000, 'gasPrice': 0x630000000})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    time.sleep(5)
    

def add(path):
    # 将照片上传至ipfs系统并记录hash
    cmd = subprocess.Popen('ipfs add -Q %s' % path, shell=True, stdout=subprocess.PIPE)
    out, err = cmd.communicate()
    for line in out.splitlines():
        return line.decode("gbk", "ignore")


def list_dir(file_dir):
    #  遍历照片夹中所有照片，调用add函数进行上传和记录，将记录到的信息录入字典
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path):
            i = add(path)
            print(i)
            file[i] = [str(cur_file), os.stat(path).st_size]
            onchain(i,str(cur_file),os.stat(path).st_size)
        if os.path.isdir(path):
            # 递归读取所有照片夹子目录内容
            list_dir(path)

def list_dir2(file_dir):
    #  遍历照片夹中所有照片，调用add函数进行上传和记录，将记录到的信息录入字典
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path):
            add(path)
            file[add(path)] = [str(cur_file),os.stat(path).st_size]
        if os.path.isdir(path):
            # 递归读取所有文件夹子目录内容
            list_dir(path)


def upload():
    unlockAccount()
    reset()
    path = './exfile'
    list_dir(path)
    with open('save.json', 'w+',encoding='utf-8') as f:
        # 打开新的json文件
        list_dir2(file_dir=r'./exfile')
    with open('save.json', 'a',encoding='utf-8') as f:
        # 将字典写入json
        json.dump(file, f,ensure_ascii=False)
    sentInfo()


if __name__ == '__main__':
    upload()
