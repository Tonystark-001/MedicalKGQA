# -*- coding:utf-8 -*-
# @Time : 2020/2/22 13:47
# @Author : TianWei
# @File : data_test.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

import json


with open("./data/medical.json","r",encoding='utf-8') as f:
	data = json.load(f)
print(list(data.values()))

