#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：cipher.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/2 15:03 
@contact :richard.eth@foxmail.com
'''
from Crypto.Cipher import AES
import base64


class AESCipher(object):
    def __init__(self, key,iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.cipher = AES.new(self.key, self.mode,self.iv)
    def encrypto(self,data):
        pading = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size).encode("utf-8")
        enc = base64.b64encode(self.cipher.encrypt(pading(data.encode("utf-8")))).decode("utf-8")
        return enc

    def decrypto(self, data):
        try:
            unpading = lambda s: s[:-ord(s[len(s) - 1:])]
            dec = unpading(self.cipher.decrypt(base64.b64decode(data)).decode('utf-8'))
        except Exception as e:
            print('error:', e)
        return dec