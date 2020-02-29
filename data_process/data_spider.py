# -*- coding:utf-8 -*-
# @Time : 2020/2/21 16:12
# @Author : TianWei
# @File : data_spider.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

import pymongo
import urllib.request
import urllib.parse
from lxml import etree
import json
import os
import utils
import logging

class MedicalSpider():
	def __init__(self):
		self.conn = pymongo.MongoClient("mongodb://localhost:27017/")  # 数据库连接
		self.db = self.conn["medical"]  # 指定数据库
		self.col = self.db['data']  # 类似关系数据库中的表
		self.num_disease = 1  # 疾病总类别数
		self.start_page = 38

		self.cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
		self.local_file_name = "../data/medical.json"
		self.local_file_path = os.path.join(self.cur_dir, self.local_file_name)
		self.log_path = os.path.join(self.cur_dir, '../log/data_spider.txt')
		self.save_epochs = 500  # 每抓取 save_epochs 个数据保存到文件

	def get_html(self, url):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
								 'Chrome/51.0.2704.63 Safari/537.36'}
		req = urllib.request.Request(url=url, headers=headers)  # 自定义请求
		res = urllib.request.urlopen(req)
		html = res.read()
		return html

	# 合并所有子文件(eg. medical_0,medical_1,medical_2...)
	def merge_all_json_file(self, num_files):
		all_data = []
		for i in range(num_files):
			file_path = os.path.join(self.cur_dir, "../data/medical_{}.json".format(i))
			all_data += list(self.load_json(file_path).values())
			self.save_to_json(all_data, self.local_file_path)

	# 把由dict组成的data_list保存到文件
	def save_to_json(self, data_list, file_path):
		with open(file_path, mode='w', encoding='utf-8') as f:
			f.write("{\n")
			for ind, data in enumerate(data_list):
				if ind == len(data_list) - 1:
					f.write("\"{}\":{}\n".format(ind, json.dumps(data, ensure_ascii=False)))
				else:
					f.write("\"{}\":{},\n".format(ind, json.dumps(data, ensure_ascii=False)))
			f.write("}")

	def load_json(self, file_path):
		with open(file_path, "r", encoding='utf-8') as f:
			data = json.load(f)
		return data

	def spider_main(self):
		data_list = []
		cnt = 0
		for page in range(self.start_page, self.start_page + self.num_disease):
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

				gaishu_data = self.gaishu_spider(gaishu_url)

				if not gaishu_data:
					logging.info(" - page {} lost.".format(page))
					continue

				cause_data = self.text_spider(cause_url)
				prevent_data = self.text_spider(prevent_url)
				symptom_data = self.symptom_spider(symptom_url)
				inspect_data = self.inspect_spider(inspect_url)
				nursing_data = self.text_spider(nursing_url)
				food_data = self.food_spider(food_url)

				data = {}
				data['gaishu_info'] = gaishu_data
				data['cause_info'] = cause_data
				data['prevent_info'] = prevent_data
				# data['complication_info'] = complication_data
				data['symptom_data'] = symptom_data
				data['inspect_info'] = inspect_data
				data['nursing_info'] = nursing_data
				data['food_info'] = food_data
				data_list.append(data)

				# if len(data_list) % self.save_epochs == 0:
				# 	file_path = os.path.join(self.cur_dir, "../data/medical_{}.json".format(cnt))
				# 	self.save_to_json(data_list, file_path)
				# 	data_list = []
				# 	cnt += 1

			except Exception as e:
				logging.info(" - {} spider main error".format(page))
			# 保存文件到本地
		# if data_list:
		# 	file_path = os.path.join(self.cur_dir, "../data/medical_{}.json".format(cnt))
		# 	self.save_to_json(data_list, file_path)

	def gaishu_spider(self, url):
		'''
		疾病概述
		:param url:
		:return: dict
		返回疾病基本信息
		'''
		html = self.get_html(url)
		selector = etree.HTML(html)
		try:
			disease_name = \
			selector.xpath("//strong[@class='db f20 fYaHei fb jib-articl-tit tc pr']/text()")[0].split("简介")[0].strip()

			if not disease_name:  # 疾病名称未知,返回空dict方便过滤
				return {}

			desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')[0].strip()
			medical_insurance = ''
			disease_ratio = ''
			susceptible_people = ''
			transmission_way = ''
			has_complication = []
			belongs_to_department = []
			treat_cycle = ''
			cure_prob = ''
			treat_cost = ''
			common_drug = []

			p_box = selector.xpath('//div[@class="mt20 articl-know"]/p')

			for p in p_box:
				p_title = p.xpath("./span[1]/text()")
				p_v = p.xpath("./span[2]/a[contains(@class,'gre')]/text()")
				if p_title:
					p_title = p_title[0]
					if p_v:
						if '并发症' in p_title:
							has_complication = p_v
							print(has_complication)
						if '常用药品' in p_title:
							common_drug = p_v
							print(common_drug)
					else:
						p_v = p.xpath("./span[2]/text()")
						if p_v:
							if '医保疾病' in p_title:
								medical_insurance = p_v[0].strip()
								# print(p_title, medical_insurance)
							elif '患病比例' in p_title:
								disease_ratio = p_v[0].strip()
								# print(p_title, disease_ratio)
							elif '易感人群' in p_title:
								susceptible_people = p_v[0].strip()
								# print(p_title, susceptible_people)
							elif '传染方式' in p_title:
								transmission_way = p_v[0].strip()
								# print(p_title, transmission_way)
							elif '就诊科室' in p_title:  # ['item1  item2 imte3']
								belongs_to_department = p_v[0].strip().split()
								# print(p_title, belongs_to_department)
							elif '治疗方式' in p_title:
								treat_way = p_v[0].strip().split()
								# print(p_title, treat_way)
							elif '治疗周期' in p_title:
								treat_cycle = p_v[0].strip()
								# print(p_title, treat_cycle)
							elif '治愈率' in p_title:
								cure_prob = p_v[0].strip()
								# print(p_title, cure_prob)
							elif '治疗费用' in p_title:
								treat_cost = p_v[0].strip()
								# print(p_title, treat_cost)

			gaishu_data = {}
			gaishu_data['name'] = disease_name  # text
			gaishu_data['desc'] = desc  # text
			gaishu_data['medical_insurance'] = medical_insurance  # text
			gaishu_data['disease_ratio'] = disease_ratio  # text
			gaishu_data['susceptible_people'] = susceptible_people  # text
			gaishu_data['transmission_way'] = transmission_way  # text
			gaishu_data['has_complication'] = has_complication  # list
			gaishu_data['belongs_to_department'] = belongs_to_department  # list
			gaishu_data['treat_way'] = treat_way  # list
			gaishu_data['treat_cycle'] = treat_cycle  # text
			gaishu_data['cure_prob'] = cure_prob  # text
			gaishu_data['common_drug'] = common_drug  # list
			gaishu_data['treat_cost'] = treat_cost  # text

		# for key, value in gaishu_data.items():
		# 	if isinstance(value,(list,tuple)):
		# 		print(key + " : ",end='')
		# 		print(value)
		# 	else:
		# 		print(key + " : " + value)
		except Exception as e :
			logging.info(" - gaishu_spider extract error. url : {}".format(url))

		return gaishu_data


	def text_spider(self, url):
		'''
		:param url:
		:return: string
		返回提取的文本信息
		'''
		html = self.get_html(url)
		selector = etree.HTML(html)
		try:
			ps = selector.xpath('//p')
			infobox = []
			for p in ps:
				info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ',
																											'').replace(
					'\t', '')
				if info:
					infobox.append(info)
		except Exception as e:
			logging.info(" - text_spider extract error. url : {}".format(url))
		return '\n'.join(infobox)


	def symptom_spider(self, url):
		'''
		疾病症状
		:param url:
		:return:dict
		返回疾病的症状关键词以及详细描述
		'''
		html = self.get_html(url)
		selector = etree.HTML(html)
		try:
			symptom_data = {}
			symptom_key_words = selector.xpath("//span[@class='db f12 lh240 mb15 ']/a/text()")

			if not symptom_key_words:  # 防止空引用
				symptom_key_words = []

			ps = selector.xpath('//p')
			detail = []
			for p in ps:
				info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ',
																											'').replace(
					'\t', '')
				detail.append(info)
			symptom_data['symptoms'] = symptom_key_words  # list
			symptom_data['symptom_detail'] = detail  # text

		except Exception as e :
			logging.info(" - symptom_spider extract error. url : {}".format(url))

		return symptom_data


	def inspect_spider(self, url):
		'''
		检查项目
		:param url:
		:return: list
		'''
		html = self.get_html(url)
		selector = etree.HTML(html)
		inspects_url = selector.xpath('//li[@class="check-item"]/a/@href')  # 获取所有要检查项目的链接

		if not inspects_url: # 防止空引用
			inspects_url = []

		inspects = []
		for inspect_url in inspects_url:
			inspect_name = self.inspect_crawl(inspect_url)
			if inspect_name.strip():
				inspects.append(inspect_name)
		# print(inspects)
		return inspects  # list


	def inspect_crawl(self, url):
		'''
		抓取检查项目详细内容
		:param url:
		:return:
		暂时抓取检查项名称
		'''
		try:
			html = self.get_html(url)
			selector = etree.HTML(html)
			data = {}
			res = selector.xpath('//div[@class="clearfix"]/strong/text()')
			if res:
				data['inspect_name'] = res[0].strip()
			else:
				data['inspect_name'] = ''
		except Exception as e:
			data['inspect_name'] = ''

			logging.info(" - inspect_crawl extract error. url : {}".format(url))
		return data['inspect_name']


	def food_spider(self, url):
		'''
		食物
		:param url:
		:return: dict
		'''
		html = self.get_html(url)
		selector = etree.HTML(html)
		try:
			diet_text_list = selector.xpath("//div[@class='fl diet-good-txt']/text()")
			good_food = selector.xpath("//div[@class='panels mt10']/div[2]//p[@class='diet-opac-txt pa f12']/text()")
			avoid_food = selector.xpath("//div[@class='panels mt10']/div[3]//p[@class='diet-opac-txt pa f12']/text()")
			recommand_recipes = selector.xpath(
				"//div[@class='panels mt10']/div[4]//p[@class='diet-opac-txt pa f12']/text()")

			if len(diet_text_list) > 1:
				good_diet_text = diet_text_list[0].strip()
				avoid_diet_text = diet_text_list[1].strip()
			else:
				good_diet_text = ''
				avoid_diet_text = ''

			food_data = {}
			food_data['good_diet_text'] = good_diet_text  # text
			food_data['avoid_diet_text'] = avoid_diet_text  # text
			food_data['recommand_recipes'] = recommand_recipes  # list
			food_data['good_food'] = good_food  # list
			food_data['avoid_food'] = avoid_food  # list

		except Exception as e:
			logging.info(" - food_spider extract error. url : {}".format(url))

		return food_data


	def remove_whitespace(self, text):
		return text.strip()


if __name__ == '__main__':

	handler = MedicalSpider()
	# utils.set_logger(handler.log_path)
	handler.spider_main()
	# handler.merge_all_json_file(18)
	# data = handler.load_json(handler.local_file_path)
