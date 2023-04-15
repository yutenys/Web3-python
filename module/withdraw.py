#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：withdraw.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/15 17:15 
@contact :richard.eth@foxmail.com
'''
from module.configHandler import HandleConfig
import okx.Account as ac,okx.Funding as fd
import time,csv,random
from module.cipher import AESCipher
from Crypto import Random
from Crypto.Cipher import AES
from module.log import get_logger

# #重写读取ini配置文件方法，解决配置文件读取后出现小写问题
# class configParse(configparser.ConfigParser):
#     def __init__(self, defaults=None):
#         configparser.ConfigParser.__init__(self, defaults=defaults)
#
#     def optionxform(self, optionstr: str) -> str:
#         return optionstr

logger = get_logger()

#批量提币
dest = "4" #3是内部转账，4是链上提币
conf = HandleConfig(r'config/config.ini')
coin = conf.config['DEFAULT']['COIN']  # 提币类型
fee = conf.config['DEFAULT']['FEE']  # 网络手续费，需要去OKX查看
chain = conf.config['DEFAULT']['CHAIN']

#模拟盘or实盘，1为模拟盘，0为实盘
flag = '0'


def getAccounts():
    try:
        with open(f'./data/withdrawAccount.csv', 'r') as f:
            reader = [x for x in csv.DictReader(f)]
        return reader
    except Exception as e:
        print("Error：",e)

def tips(coin,chain,reader):
    amount = 0
    for address in reader:
        amount += float(address['amount'])
    p = f'请注意：当前正在提取【{coin}】到【{chain}】链上，共{len(reader)}个地址，{amount}个{coin}等待提币(未统计随机数)'
    print(p)
    logger.info(p)

def withdraw(funding,reader,coin,dest,fee,chain):
    for i in range(len(reader)):
        address = reader[i]['account']
        amount = reader[i]['amount'] #固定提取额度
        if reader[i]['add'] != None and len(reader[i]['add']) > 0 : #启用固定金额+随机小金额
            adds = reader[i]['add'].split('/')
            amount = round(float(amount) + random.uniform(float(adds[0]),float(adds[1])),6)
        elif reader[i]['rand'] != None and len(reader[i]['rand']) > 0 : #启用随机金额
            adds = reader[i]['rand'].split('/')
            amount = round(random.uniform(float(adds[0]),float(adds[1])),6)
        while True:
            try:
                result = funding.withdrawal(ccy=coin,amt=str(amount),dest=dest,toAddr=address,fee=fee,chain=chain)
                if result['code'] != '0':
                    p = f'{address}】提币失败！--{result}'
                    print(p)
                    logger.info(p)
                else:
                    p = f'{i + 1}---【{address}】提币【{amount}】{coin} 到【{chain}】链成功！'
                    print(p)
                    logger.info(p)
                break
            except Exception as e:
                p = f'{address}】提币失败！{e}'
                print(p)
                logger.info(p)
                time.sleep(random.randint(5,10))
        time.sleep(random.randint(1,10)) #提币随机等待时间
def getBalance(funding,ccy):
    try:
        result = funding.get_balances(ccy="ETH")
        p = f"账号{result['data'][0]['ccy']}余额：{result['data'][0]['availBal']}"
        print(p)
        logger.info(p)
    except Exception as e:
        print(f'查询余额失败:{e}')
        logger.info(f'查询余额失败:{e}')

def log(path,content):
    with open(path,'a+') as f:
        f.write(content + '\n')
        f.close()

def encrypt_file():
    conf = HandleConfig(r'config/config.ini')
    api_key = ''
    secret_key = ''
    passphrase = ''
    iv = ''
    if len(conf.config.sections()) > 0:
        for sec in conf.config.sections():
            if conf.config.has_option(section=sec,option='API_KEY') and len(conf.config[sec]['API_KEY']) != 0 :
                api_key = conf.config[sec]['API_KEY']
            if conf.config.has_option(section=sec,option='SECRET_KEY') and len(conf.config[sec]['SECRET_KEY']) != 0:
                secret_key = conf.config[sec]['SECRET_KEY']
            if conf.config.has_option(section=sec,option='PASSPHRASE') and len(conf.config[sec]['PASSPHRASE']) != 0:
                passphrase = conf.config[sec]['PASSPHRASE']
    else:
        if len(conf.config['DEFAULT']['API_KEY']) != 0:
            api_key = conf.config['DEFAULT']['API_KEY']
        if len(conf.config['DEFAULT']['SECRET_KEY']) != 0:
            secret_key = conf.config['DEFAULT']['SECRET_KEY']
        if len(conf.config['DEFAULT']['PASSPHRASE']) != 0:
            passphrase = conf.config['DEFAULT']['PASSPHRASE']
    if api_key != 0 and secret_key != 0 and passphrase != 0:
        if 'richard_' in api_key or 'richard_' in secret_key or 'richard_' in passphrase:
            print('已经加密过了')
            logger.info('已经加密过了')
        else:
            print('----------准备加密----------')
            logger.info('----------准备加密----------')
            key = bytes(input('请输入16位或者16的倍数位密码:'),encoding='utf-8')
            if len(conf.config['DEFAULT']['IV']) > 0:
                iv = conf.config['DEFAULT']['IV']
            else:
                iv = Random.new().read(AES.block_size).hex()
            try:
                encp = AESCipher(key, bytes.fromhex(iv))
                conf.set('DEFAULT', 'IV', iv)
                conf.set('DEFAULT', 'API_KEY', 'richard_' + encp.encrypto(conf.config['DEFAULT']['API_KEY']))
                conf.set('DEFAULT', 'SECRET_KEY', 'richard_' + encp.encrypto(conf.config['DEFAULT']['SECRET_KEY']))
                conf.set('DEFAULT', 'PASSPHRASE', 'richard_' + encp.encrypto(conf.config['DEFAULT']['PASSPHRASE']))
                conf.config.write(open("./Config/config.ini", 'w'))
                print('----------加密完成----------')
                logger.info('----------加密完成----------')
            except Exception as e:
                if 'Incorrect AES key length' in e.__str__():
                    print('输入的密码位数错误，需要位16位或者16的倍数位')
                    logger.info('输入的密码位数错误，需要位16位或者16的倍数位')
                else:
                    print(f'加密失败：{e}')
                    logger.info(f'加密失败：{e}')
    else:
        print('API_KEY，SECRET_KEY，PASSPHRASE三个都需要配置，缺一不可！')
        logger.info('API_KEY，SECRET_KEY，PASSPHRASE三个都需要配置，缺一不可！')

def decrypt_file():
    conf = HandleConfig(r'config/config.ini')
    if len(conf.config.sections()) > 0:
        for sec in conf.config.sections():
            if conf.config.has_option(section=sec, option='API_KEY') and len(conf.config[sec]['API_KEY']) != 0:
                api_key = conf.config[sec]['API_KEY']
            if conf.config.has_option(section=sec, option='SECRET_KEY') and len(conf.config[sec]['SECRET_KEY']) != 0:
                secret_key = conf.config[sec]['SECRET_KEY']
            if conf.config.has_option(section=sec, option='PASSPHRASE') and len(conf.config[sec]['PASSPHRASE']) != 0:
                passphrase = conf.config[sec]['PASSPHRASE']
    else:
        if len(conf.config['DEFAULT']['API_KEY']) != 0:
            api_key = conf.config['DEFAULT']['API_KEY']
        if len(conf.config['DEFAULT']['SECRET_KEY']) != 0:
            secret_key = conf.config['DEFAULT']['SECRET_KEY']
        if len(conf.config['DEFAULT']['PASSPHRASE']) != 0:
            passphrase = conf.config['DEFAULT']['PASSPHRASE']
    if api_key != 0 and secret_key != 0 and passphrase != 0:
        if 'richard_' in api_key or 'richard_' in secret_key or 'richard_' in passphrase:
            key = bytes(input('请输入16位或者16的倍数位的解密密码:'), encoding='utf-8')
            try:
                decp = AESCipher(key, bytes.fromhex(conf.config['DEFAULT']['IV']))
                api_key = decp.decrypto(conf.config['DEFAULT']['API_KEY'].replace('richard_',''))
                secret_key = decp.decrypto(conf.config['DEFAULT']['SECRET_KEY'].replace('richard_',''))
                passphrase = decp.decrypto(conf.config['DEFAULT']['PASSPHRASE'].replace('richard_',''))
                print('配置文件:',api_key,secret_key,passphrase)
                return api_key, secret_key, passphrase
            except Exception as e:
                if 'Incorrect AES key length' in e.__str__():
                    print('输入的密码位数错误，需要位16位或者16的倍数位')
                    logger.info('输入的密码位数错误，需要位16位或者16的倍数位')
                elif "local variable 'dec' referenced before assignment" in e.__str__():
                    print('密码错误或者配置文件中的加密串异常！')
                    logger.info('密码错误或者配置文件中的加密串异常！')
                else:
                    print(f'解密失败：{e}')
                    logger.info(f'解密失败：{e}')
        else:
            print('未加密！')
            logger.info('未加密！')
    else:
        print('API_KEY，SECRET_KEY，PASSPHRASE三个都需要配置，缺一不可！')
        logger.info(f'API_KEY，SECRET_KEY，PASSPHRASE三个都需要配置，缺一不可！')

