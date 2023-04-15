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
import module.withdraw as wd



if __name__ == '__main__':
    #1111111111111111
    help = '''
    **********指令说明**********
    *输入'1'批量创建钱包
    *输入'2'批量加密钱包
    *输入'3'批量解密钱包
    *输入'4'加密配置文件
    *输入'5'解密配置文件
    *输入'6'okx批量提现
    *输入'7'查询okx余额
    *输入'0'或者'h'或者'help'唤出功能说明
    ***************************'''
    print(help)

    w = Wallet()
    while True:
        k = input("请输入你要执行的操作：")
        if k == '1':
            print('【正在执行操作】：创建钱包')
            w.creatWallets()
        elif k == '2':
            print('【正在执行操作】：加密钱包')
            w.enWallets()
        elif k == '3':
            print('【正在执行操作】：解密钱包')
            w.deWallet()
        elif k == '4':
            print('【正在执行操作】：加密配置文件')
            wd.encrypt_file()
        elif k == '5':
            print('【正在执行操作】：解密配置文件')
            wd.decrypt_file()
        elif k == '6':
            print('【正在执行操作】：从okx提现')
            conf = wd.decrypt_file()
            if conf == None:
                print('提币失败')
            else:
                reader = wd.getAccounts()
                wd.tips(wd.coin, wd.chain, reader)
                funding = wd.fd.FundingAPI(conf[0], conf[1], conf[2], False,
                                        wd.flag, debug=False)
                inp = input('是否继续(y/n)：')
                if inp == 'y':
                    wd.withdraw(funding, reader, wd.coin, wd.dest, wd.fee, wd.chain)
                else:
                    print('未提币')
        elif k == '7':
            print('【正在执行操作】：查询okx余额')
            ccy = input('请输入要查询的资产代码:')
            try:
                conf = wd.decrypt_file()
                print('conf[0]：',conf[0])
                funding = wd.fd.FundingAPI(conf[0], conf[1], conf[2], False,
                                           wd.flag, debug=False)
                wd.getBalance(funding, ccy)
            except Exception as e:
                print('Error:',e)
        elif k == '0' or k == 'h' or k == 'help':
            print(help)
        else:
            print('你输入的指令当前还不支持！')