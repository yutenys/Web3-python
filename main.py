#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：main.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/2 17:33 
@contact :richard.eth@foxmail.com
'''
from module.wallets import Wallet



if __name__ == '__main__':
    #1111111111111111
    help = '''
    **********指令说明**********
    *输入'1'批量创建钱包
    *输入'2'批量加密钱包
    *输入'3'批量解密钱包
    *输入'4'唤出功能说明
    ***************************'''
    print(help)

    w = Wallet()
    while True:
        k = input("请输入你要执行的操作：")
        if k == '1':
            w.creatWallets()
        elif k == '2':
            w.enWallets()
        elif k == '3':
            w.deWallet()
        elif k == '4':
            print(help)
        else:
            print('你输入的指令当前还不支持！')