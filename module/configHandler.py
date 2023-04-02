#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：web3 
@File    ：configHandler.py
@Author  ：Richard
@License ：(C) Copyright 2021-2022, Richard.
@Date    ：2023/4/2 15:11 
@contact :richard.eth@foxmail.com
'''
from module.reConfigParser import ReConfigParser

class HandleConfig():
    def __init__(self):
        self.filename = r'config/config.ini'
        self.config = ReConfigParser()
        self.config.read(self.filename)

    # 重写读取ini配置文件方法，解决配置文件读取后出现小写问题
    def optionxform(self, optionstr: str) -> str:
        return optionstr

    # get_value获取所有的字符串，section区域名, option选项名
    def get_value(self,section,option):
        return self.config.get(section,option)

    # get_int获取所有的整数，section区域名, option选项名
    def get_int(self,section,option):
        return self.config.getint(section,option)

    # get_float获取浮点数类型，section区域名, option选项名
    def get_float(self, section, option):
        return self.config.getfloat(section, option)

    # get_boolean（译：比例恩）获取布尔类型，section区域名, option选项名
    def get_boolean(self, section, option):
        return self.config.getboolean(section, option)

    # get_eval_data 获取列表，section区域名, option选项名
    def get_eval_data(self, section, option):
        return eval(self.config.get(section, option))  # get 获取后为字符串，再用 eval 转换为列表

    def set(self, field, key, value):
        try:
            self.config.set(field, key, value)
            self.config.write(open(self.filename,'w'))  # 创建一个配置文件并将获取到的配置信息使用配置文件对象的写入方法进行写入
            return True
        except Exception as e:
            print("save config error:",e)
            return False

    def write_config(self,datas):
        """
        写入配置操作
        :param datas: 需要传入写入的数据
        :param filename: 指定文件名
        :return:
        """
        # 做校验，为嵌套字典的字典才可以（意思.隐私.谈.ce)
        if isinstance(datas, dict):  # 遍历，在外层判断是否为字典
            # 再来判断内层的 values 是否为字典
            for value in datas.values():  # 先取出value
                if not isinstance(value, dict):  # 在判断
                    return "数据不合法, 应为嵌套字典的字典"

            for key in datas:  # 写入操作
                self.config[key] = datas[key] # config 类似于一个空字典
                self.config.write(open(self.filename, 'w'))


# if __name__ == '__main__':
        # # 读取操作
        # do_config1 = HandleConfig()  # 读取那个文件
        # res = do_config1.get_value("MSG", "SUCC")  # 读取什么内容
        # print(res)
        #
        # # do_config1.set('DEFAULT','kkk','VVV')
        #
        # # 写入操作
        # do_config = HandleConfig()
        # datas = {
        #     "DEFAULT": {
        #         "CASE1": "cases.xlsx",
        #         "LOG1": "record_run_result.txt"
        #     },
        #     "MSG": {
        #         "SUCC1": "Pass",
        #         "FAIL1": "Fail"
        #     }
        # }
        # do_config.write_config(datas)