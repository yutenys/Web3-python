#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：log.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/15 17:14 
@contact :richard.eth@foxmail.com
'''
import logging
import datetime
import os


def get_logger():
    # 创建logger对象
    logger = logging.getLogger("executed_logger")
    # 设置日志等级
    logger.setLevel(logging.DEBUG)
    # 追加写入文件，设置utf-8编码防止中文乱码
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    projectPath = os.getcwd()
    file_name = projectPath + '/logs/' + 'executed_' + day + '.log'
    executed_log = logging.FileHandler(file_name, 'a', encoding='utf-8')
    # 向文件输出的日志级别
    executed_log.setLevel(logging.DEBUG)
    # 向文件输出的日志信息格式
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s - %(message)s -%(process)s')
    executed_log.setFormatter(formatter)
    # 加载文件到logger对象中
    logger.addHandler(executed_log)
    return logger

