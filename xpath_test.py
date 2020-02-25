# -*- coding:utf-8 -*-
# @Time : 2020/2/21 21:16
# @Author : TianWei
# @File : xpath_test.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com


# sql = ["hello {}".format(i) for i in range(5)]
# print(sql)
# question = "睡眠并发症"
# complication_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
#
#
# def check_qwds_type(words, sent):
# 	'''基于特征词进行分类'''
# 	for word in words:
# 		if word in sent:
# 			return True
# 	return False
#
# if check_qwds_type(complication_qwds,question):
# 	print("True")
# else:
# 	print("False")

import json
with open("./data/medical.json","r",encoding='utf-8') as f:
	data = json.load(f)
print(len(data))
# import urllib
# from lxml import etree
#
# def get_html(url):
# 	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
# 							 'Chrome/51.0.2704.63 Safari/537.36'}
# 	req = urllib.request.Request(url=url, headers=headers)  # 自定义请求
# 	res = urllib.request.urlopen(req)
# 	html = res.read()
# 	return html
#
# url = 'http://jib.xywy.com/il_sii/gaishu/11000.htm'
# url2 = 'http://jib.xywy.com/il_sii/gaishu/1.htm'
# html = get_html(url2)
# selector = etree.HTML(html)
#
# p_box = selector.xpath('//div[@class="mt20 articl-know"]/p')
#
# for p in p_box:
# 	p_title = p.xpath("./span[1]/text()")
# 	p_v = p.xpath("./span[2]/a[contains(@class,'gre')]/text()")
# 	if p_title:
# 		p_title = p_title[0]
# 		if p_v:
# 			if '并发症' in p_title:
# 				has_complication = p_v
# 				print(p_title,has_complication)
# 			elif '常用药品' in p_title:
# 				common_drug = p_v
# 				print(p_title,common_drug)
# 		else:
# 			p_v = p.xpath("./span[2]/text()")
# 			if p_v:
# 				if '医保疾病' in p_title:
# 					medical_insurance = p_v[0].strip()
# 					print(p_title,medical_insurance)
# 				elif '患病比例' in p_title:
# 					disease_ratio = p_v[0].strip()
# 					print(p_title, disease_ratio)
# 				elif '易感人群' in p_title:
# 					susceptible_people = p_v[0].strip()
# 					print(p_title,susceptible_people)
# 				elif '传染方式' in p_title:
# 					transmission_way = p_v[0].strip()
# 					print(p_title,transmission_way)
# 				elif '就诊科室' in p_title:  # ['item1  item2 imte3']
# 					belongs_to_department = p_v[0].strip().split()
# 					print(p_title,belongs_to_department)
# 				elif '治疗方式' in p_title:
# 					treat_way = p_v[0].strip().split()
# 					print(p_title,treat_way)
# 				elif '治疗周期' in p_title:
# 					treat_cycle = p_v[0].strip()
# 					print(p_title,treat_cycle)
# 				elif '治愈率' in p_title:
# 					cure_prob = p_v[0].strip()
# 					print(p_title,cure_prob)
# 				elif '治疗费用' in p_title:
# 					treat_cost = p_v[0].strip()
# 					print(p_title,treat_cost)









