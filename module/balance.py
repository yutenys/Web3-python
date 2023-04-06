#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：balance.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/6 20:10 
@contact :richard.eth@foxmail.com
'''

from web3 import Web3, HTTPProvider

class getBalance():

    def read_file(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            data = f.readlines()
        return data

    def check_balance(self,chain, type, address):
        rpcs = {
            "ETH": "https://cloudflare-eth.com",
            "BSC": "https://bsc-dataseed1.binance.org:443",
            "Ploygon":"https://polygon.llamarpc.com"
        }
        print(rpcs[chain])
        web3 = Web3(HTTPProvider(rpcs[chain]))
        balance = web3.fromWei(web3.eth.get_balance(address), "ether")
        print(f"账户 {address} 【{chain}】链的{type}余额是: {balance} ")
        return balance