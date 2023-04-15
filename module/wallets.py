#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：wallets.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/2 15:05 
@contact :richard.eth@foxmail.com
'''
import time
import random
from eth_account import Account
from module.cipher import AESCipher
from Crypto import Random
from Crypto.Cipher import AES
from module.configHandler import HandleConfig
import os
class Wallet():
    def creatWallets(self):
        # 生成钱包地址
        walletnum = input("请输入需要的钱包数量:")
        aa = []
        conf = HandleConfig(r'config/config.ini')
        time.sleep(random.randint(3,5)/1000)
        for i in range(int(walletnum)):
            aa.append(self.createAccount(i))
        self.addwrite(conf.config['DEFAULT']['WalletPath'],aa)
        print(f"{walletnum}个钱包已完成创建")
    @staticmethod
    def createAccount(index):
        Account.enable_unaudited_hdwallet_features()
        account, mnemonic = Account.create_with_mnemonic()
        privateKey = account._key_obj
        publicKey = privateKey.public_key
        address = publicKey.to_checksum_address()
        return str(index+1),address,str(privateKey)
    @staticmethod
    def addwrite(path,data):
        with open(path, 'w') as f:
            for i in range(len(data)):
                line = data[i][0] + ',' + data[i][1] + ',' + data[i][2] + '\n'
                f.write(line)

    def enWallets(self):
        conf = HandleConfig(r'config/config.ini')
        wallets = conf.config['DEFAULT']['WalletPath']
        en_wallets = conf.config['DEFAULT']['EN_WalletPath']
        if os.path.exists(wallets) == False:
            print('请检查配置，确保需要加密的钱包文件存在！')
        else:
            key = bytes(input('请输入16位或者16的倍数位密码:'), encoding='utf-8')
            iv = ''
            if conf.config.has_option(section='DEFAULT', option='IV'):
                if len(conf.config['DEFAULT']['IV']) > 0:
                    iv = conf.config['DEFAULT']['IV']
                else:
                    iv = Random.new().read(AES.block_size).hex()
                    conf.set('DEFAULT', 'IV', iv)
            else:
                iv = Random.new().read(AES.block_size).hex()
                conf.set('DEFAULT', 'IV', iv)
            final = []
            try:
                encp = AESCipher(key, bytes.fromhex(iv))
                with open(wallets, 'r') as f:
                    for line in f.readlines():
                        temp = []
                        temp.append(line.split(',')[0])
                        temp.append(line.split(',')[1])
                        temp.append(encp.encrypto(line.split(',')[2].strip()))
                        final.append(temp)
                self.addwrite(en_wallets, final)
                print('加密完成！')
            except Exception as e:
                if 'Incorrect AES key length' in e.__str__():
                    print('输入的密码位数错误，需要位16位或者16的倍数位')
                else:
                    print(f'加密失败：{e}')

    def deWallet(self):
        conf = HandleConfig(r'config/config.ini')
        de_wallets = conf.config['DEFAULT']['DE_WalletPath']
        en_wallets = conf.config['DEFAULT']['EN_WalletPath']
        if os.path.exists(en_wallets) == False:
            print('请检查配置，确保需要解密的钱包文件存在！')
        else:
            key = bytes(input('请输入16位或者16的倍数位密码:'), encoding='utf-8')
            iv = ''
            if conf.config.has_option(section='DEFAULT', option='IV'):
                if len(conf.config['DEFAULT']['IV']) > 0:
                    iv = conf.config['DEFAULT']['IV']
                else:
                    iv = Random.new().read(AES.block_size).hex()
                    conf.set('DEFAULT', 'IV', iv)
            else:
                iv = Random.new().read(AES.block_size).hex()
                conf.set('DEFAULT', 'IV', iv)
            final = []
            try:
                encp = AESCipher(key, bytes.fromhex(iv))
                with open(en_wallets, 'r') as f:
                    for line in f.readlines():
                        temp = []
                        temp.append(line.split(',')[0])
                        temp.append(line.split(',')[1])
                        temp.append(encp.decrypto(line.split(',')[2].strip()))
                        final.append(temp)
                self.addwrite(de_wallets, final)
                print('解密完成！')
            except Exception as e:
                if 'Incorrect AES key length' in e.__str__():
                    print('输入的密码位数错误，需要位16位或者16的倍数位')
                else:
                    print(f'解密失败：{e}')
