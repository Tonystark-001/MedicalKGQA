# -*- coding:utf-8 -*-
# @Time : 2020/2/22 21:59
# @Author : TianWei
# @File : test_mongodb.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com
import os
import py2neo
import pymongo
import urllib

class MedicalSpider():
	def __init__(self):
		self.conn = pymongo.MongoClient("mongodb://localhost:27017/")  # 数据库连接
		self.db = self.conn["medical"]  # 指定数据库
		self.col = self.db['data']  # 类似关系数据库中的表
		self.num_disease = 100  # 疾病总类别数
		self.start_page = 1
		self.cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
		self.local_file_name = "../data/medical.json"
		self.local_file_path = os.path.join(self.cur_dir,self.local_file_name)
	def get_html(self, url):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
								 'Chrome/51.0.2704.63 Safari/537.36'}
		req = urllib.request.Request(url=url, headers=headers)  # 自定义请求
		res = urllib.request.urlopen(req)
		html = res.read()
		return html

	def spider_main(self):
		data_list = []
		for page in range(self.start_page,self.start_page+self.num_disease):
			try:
				print("this is page {}".format(page))
				gaishu_url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm' % page
				cause_url = 'http://jib.xywy.com/il_sii/cause/%s.htm' % page
				prevent_url = 'http://jib.xywy.com/il_sii/prevent/%s.htm' % page
				# complication_url = 'http://jib.xywy.com/il_sii/neopathy/%s.htm' % page  信息在gaishu里面提取过了
				symptom_url = 'http://jib.xywy.com/il_sii/symptom/%s.htm' % page
				inspect_url = 'http://jib.xywy.com/il_sii/inspect/%s.htm' % page
				# treat_url = 'http://jib.xywy.com/il_sii/treat/%s.htm' % page # 信息在gaishu里面提取过了
				nursing_url = 'http://jib.xywy.com/il_sii/nursing/%s.htm' % page
				food_url = 'http://jib.xywy.com/il_sii/food/%s.htm' % page

				data = {}

			except Exception as e:
				print("{} in {}".format(e, page))
