#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：reConfigParser.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/15 20:28 
@contact :richard.eth@foxmail.com
'''
from configparser import ConfigParser
class ReConfigParser(ConfigParser):
    def __init__(self,defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    # 重写读取ini配置文件方法，解决配置文件读取后出现小写问题
    def optionxform(self, optionstr: str) -> str:
        return optionstr