# -*- coding:utf-8 -*-
# @Time : 2020/2/23 14:20
# @Author : TianWei
# @File : question_classification.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

import os
import ahocorasick
import logging

class QuestionClassifier(object):
	def __init__(self):
		# self.cur_dir = "/".join(os.path.abspath(__file__).split("/")[:-1])
		if "MedicalKGQA" not in os.path.abspath(os.path.dirname(os.getcwd())):
			self.project_dir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),"MedicalKGQA")
		else:
			self.project_dir = os.path.abspath(os.path.dirname(os.getcwd()))
		print("project dir : ", self.project_dir)
		self.log_path = os.path.join(self.project_dir, 'log/question_classification.txt')
		# 特征词路径
		self.disease_path = os.path.join(self.project_dir, 'region_words/diseases.txt')
		self.department_path = os.path.join(self.project_dir, 'region_words/departments.txt')
		self.check_path = os.path.join(self.project_dir, 'region_words/checks.txt')
		self.drug_path = os.path.join(self.project_dir, 'region_words/drugs.txt')
		self.food_path = os.path.join(self.project_dir, 'region_words/foods.txt')
		self.symptom_path = os.path.join(self.project_dir, 'region_words/symptoms.txt')
		self.deny_path = os.path.join(self.project_dir, 'region_words/deny.txt')

		# 加载特征词
		self.disease_words = [word.strip() for word in open(self.disease_path, encoding='utf-8') if word.strip()]
		self.department_words = [word.strip() for word in open(self.department_path, encoding='utf-8') if word.strip()]
		self.check_words = [word.strip() for word in open(self.check_path, encoding='utf-8') if word.strip()]
		self.drug_words = [word.strip() for word in open(self.drug_path, encoding='utf-8') if word.strip()]
		self.food_words = [word.strip() for word in open(self.food_path, encoding='utf-8') if word.strip()]
		self.symptom_words = [word.strip() for word in open(self.symptom_path, encoding='utf-8') if word.strip()]

		self.deny_words = [word.strip() for word in open(self.deny_path, encoding='utf-8') if word.strip()]

		# 领域特种词
		self.region_words = set(self.disease_words + self.department_words + self.check_words
								+ self.drug_words + self.food_words + self.symptom_words)  # type:set
		# 构造领域actree
		self.region_tree = self.build_actree(list(self.region_words))

		# 构建词典
		self.word_type_dict = self.build_word_type_dict()

		# 问句疑问词
		self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现','什么样']
		self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致',
						   '会造成','怎么回事','总是','老是']
		self.complication_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
		self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
		self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片','什么药']
		self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
							 '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
							 '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
							 '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
							 '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
		self.treat_cycle_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
		self.treat_way_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治','治疗方式']
		self.cure_prob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医','概率']
		self.susceptible_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
		self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出','怎么查','查什么']
		self.belong_qwds = ['属于什么科', '属于', '什么科', '科室','挂号','挂什么','挂什么科室']
		self.effect_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
						  '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要','能干啥']
		self.treat_cost_qwds = ['多少钱','开销','花费','治疗费用','多少钱','费用']
		self.medical_insurance_qwds = ['报销','医保','报销比例','合作医疗']
		self.transmission_way_qwds = ['怎么传播','传播','传染']
		self.nursing_qwds = ['护理','如何护理','护理方式','护理方法','保养']

		logging.info(" - model init finished.")

	def classify_main(self,question):
		'''
		:param question:
		:return: dict
		keywords : 问题中的关键词以及其对应实体类型（标签）
		question_types : 根据关键词及问题词（qwds） 判断问句类别（eg。 已知疾病找药物）
		'''
		keywords = self.get_keyword_from_question(question) # 以(region_wd, [type_list]) 形式返回问题中包含的领域词及类型

		if not keywords: # 如果问句中没有匹配的关键词，则无效问题（无法回答）
			return {}

		data = {}
		data['keywords'] = keywords
		types = []
		# 收集问句当中所涉及到的实体类型
		for type in keywords.values():
			types += type

		question_type = 'Others'
		question_types = []


		# 已知疾病判断症状
		if self.check_qwds_type(self.symptom_qwds,question) and('Disease' in types):
			question_type = 'disease_symptom'
			question_types.append(question_type)

		# 已知症状判断疾病
		if self.check_qwds_type(self.symptom_qwds,question) and ('Symptom' in types):
			question_type = 'symptom_disease'
			question_types.append(question_type)

		# 疾病原因
		if self.check_qwds_type(self.cause_qwds,question) and ('Disease' in types):
			question_type = 'disease_cause'
			question_types.append(question_type)

		# 并发症
		if self.check_qwds_type(self.complication_qwds,question) and ('Disease' in types):
			question_type = 'disease_complication'
			question_types.append(question_type)

		# 疾病常用药品
		if self.check_qwds_type(self.drug_qwds,question) and ('Disease' in types):
			question_type = 'disease_drug'
			question_types.append(question_type)

		# 药物治疗啥病
		if self.check_qwds_type(self.effect_qwds,question) and ('Drug' in types):
			question_type = 'drug_disease'
			question_types.append(question_type)

		# 已知疾病推荐或拒绝食物
		if not self.check_qwds_type(self.drug_qwds,question) and self.check_qwds_type(self.food_qwds,question) and ('Disease' in types):
			is_deny = self.check_qwds_type(self.deny_words,question)
			if is_deny:
				question_type = "disease_avoid_food"
			else:
				question_type = "disease_good_food" # 包括推荐食物，以及食谱
			question_types.append(question_type)

		# 已知食物找疾病
		if self.check_qwds_type(self.food_qwds + self.effect_qwds,question) and ("Food" in types):
			is_deny = self.check_qwds_type(self.deny_words, question)
			if is_deny:
				question_type = "food_avoid_disease"
			else:
				question_type = "food_good_disease"
			question_types.append(question_type)


		# 疾病检查项目
		if self.check_qwds_type(self.check_qwds,question) and ('Disease' in types):
			question_type ='disease_check'
			question_types.append(question_type)

		# 已知检查项目查相应疾病
		if self.check_qwds_type(self.check_qwds + self.effect_qwds,question) and ('Check' in types):
			question_type = 'check_disease'
			question_types.append(question_type)

		# 疾病预防
		if self.check_qwds_type(self.prevent_qwds,question) and ('Disease' in types):
			question_type = 'disease_prevent'
			question_types.append(question_type)

		# 疾病治疗方法
		if self.check_qwds_type(self.treat_way_qwds,question) and ('Disease' in types):
			question_type = 'disease_treat_way'
			question_types.append(question_type)

		# 疾病治愈可能性
		if self.check_qwds_type(self.cure_prob_qwds,question) and ('Disease' in types):
			question_type = 'disease_cure_prob'
			question_types.append(question_type)

		# 疾病易感人群
		if self.check_qwds_type(self.susceptible_qwds,question) and ('Disease' in types):
			question_type = 'disease_susceptible_people'
			question_types.append(question_type)

		# 疾病去哪个科室
		if self.check_qwds_type(self.belong_qwds,question) and ('Disease' in types):
			question_type = 'disease_department'
			question_types.append(question_type)

		# 疾病治疗费用
		if self.check_qwds_type(self.treat_cost_qwds,question) and ('Disease' in types):
			question_type = 'disease_treat_cost'
			question_types.append(question_type)

		# 疾病是否医保
		if self.check_qwds_type(self.medical_insurance_qwds,question) and ('Disease' in types):
			question_type = 'disease_medical_insurance'
			question_types.append(question_type)

		# 疾病治疗周期
		if self.check_qwds_type(self.treat_cycle_qwds,question) and ('Disease' in types):
			question_type = 'disease_treat_cycle'
			question_types.append(question_type)

		# 疾病传播方式
		if self.check_qwds_type(self.transmission_way_qwds,question) and ('Disease' in types):
			question_type = 'disease_transmission_way'
			question_types.append(question_type)

		# TODO 疾病护理方法
		if self.check_qwds_type(self.nursing_qwds,question) and ('Disease' in types):
			question_type = 'disease_nursing_way'
			question_types.append(question_type)

		# 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
		if question_types == [] and 'Disease' in types:
			question_types = ['disease_desc']

		# 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
		if question_types == [] and 'Symptom' in types:
			question_types = ['symptom_disease']

		# 将多个分类结果进行合并处理，组装成一个字典
		data['question_types'] = question_types
		return data

	def get_keyword_from_question(self,question):
		region_words = []
		for item in self.region_tree.iter(question):
			keyword = item[1][1]
			region_words.append(keyword)

		region_words = list(set(region_words)) # 去重

		stop_words = []
		for wd1 in region_words:
			for wd2 in region_words:
				if wd1 in wd2 and wd1 != wd2:
					stop_words.append(wd1)

		final_words = [word for word in region_words if word not in stop_words]
		final_word_types = {word:self.word_type_dict.get(word) for word in final_words}
		return final_word_types


	def build_actree(self, word_list):
		'''
				构造actree，加速过滤
				把所有的领域关键词，疾病、症状、检查等构造trie树，方便在给定的
				输入问句下快速查找所包含的关键词
			'''
		actree = ahocorasick.Automaton()

		for ind, word in enumerate(word_list):
			actree.add_word(word, (ind, word))
		actree.make_automaton()

		return actree

	def build_word_type_dict(self):
		'''
		:return: dict
		一个词可能对应多种标签类型 (eg. 肺栓塞 ['Disease', 'Symptom'])
		'''
		word_dict = dict()
		for word in self.region_words:
			word_dict[word] = []
			if word in self.disease_words:
				word_dict[word].append("Disease")

			if word in self.department_words:
				word_dict[word].append("Department")

			if word in self.check_words:
				word_dict[word].append("Check")

			if word in self.drug_words:
				word_dict[word].append("Drug")

			if word in self.food_words:
				word_dict[word].append("Food")

			if word in self.symptom_words:
				word_dict[word].append("Symptom")
		return word_dict

	def check_qwds_type(self,words,sent):
		'''基于特征词进行分类'''
		for word in words:
			if word in sent:
				return True
		return False

import stanfordcorenlp

if __name__ == '__main__':
	handler = QuestionClassifier()
	tree = handler.build_actree(['a','ab','b','c',"hello"])
	region_words = []
	for item in tree.iter("aabc"):
		key,word = item[0],item[1][1]
		region_words.append(word)
	region_words = list(set(region_words))
	print(region_words)



	# for k,v in handler.word_type_dict.items():
	# 	print(k,end='')
	# 	print(" : ",end='')
	# 	print(v)

