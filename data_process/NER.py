# -*- coding:utf-8 -*-
# @Time : 2020/2/25 18:44
# @Author : TianWei
# @File : NER.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

import jieba
import jieba.posseg as pseg
import os


class NameEntityRecogition(object):
	def __init__(self):
		self.project_dir = os.path.abspath(os.path.dirname(os.getcwd()))
		self.region_dict_path = os.path.join(self.project_dir,"region_words","region_dict")
		self.jieba = jieba
		self.jieba.load_userdict(self.region_dict_path)

	def get_user_dict(self):
		'''
		获得用户词典，保存下来
		:return:
		'''
		region_words_dir = os.path.join(self.project_dir,"region_words")
		all_words = []
		for file_name in os.listdir(region_words_dir):
			if file_name != "deny.txt":
				with open(os.path.join(region_words_dir,file_name),"r",encoding='utf-8') as f:
					for word in f.readlines():
						all_words.append(word.strip())
		with open(self.region_dict_path,"w",encoding='utf-8') as f:
			for word in all_words:
				f.write(word + "\n")

	def get_possible_entities(self,question):
		words = pseg.cut(question)
		print(question + " : ",end='')
		possible_entities = []
		for word, flag in words:
			print(word,flag)
			if "n" in flag or "x"in flag:
				possible_entities.append(word)
		print(possible_entities)
		return possible_entities

if __name__ == '__main__':
	handler = NameEntityRecogition()
	# handler.get_user_dict()
	q1 = "乳腺癌的症状有哪些？"
	q2 = "最近老流鼻涕怎么办？"
	q3 = "为什么有的人会失眠？"
	q4 = "失眠有哪些并发症？"
	q5 = "耳鸣了吃点啥？"
	q6 = "哪些人最好不好吃蜂蜜？"
	q7 = "鹅肉有什么好处？"
	q8 = "肝病要吃啥药？"
	q9 = "板蓝根颗粒能治啥病？"
	q10 = "脑膜炎怎么才能查出来？"
	q11 = "怎样才能预防肾虚？"
	q12 = "感冒要多久才能好？"
	q13 = "高血压要怎么治？"
	q14 = "白血病能治好吗？"
	q15 = "什么人容易得高血压？"
	q16 = "全血细胞计数能查出啥来"
	q17 = "糖尿病"
	q18 = "中国人的大学"
	q19 = "尿酸度能查出什么"
	q20 = "杏香兔耳风胶囊能治疗什么"
	for i in range(1,21):
		q_name = "q{}".format(i)
		question = locals()[q_name]
		possible_entities = handler.get_possible_entities(question)

