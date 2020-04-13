# -*- coding:utf-8 -*-
# @Time : 2020/2/23 19:19
# @Author : TianWei
# @File : question_parser.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

class QuestionParser(object):
	def __init__(self):
		pass

	def extract_entity(self,keywords):
		'''
		:param keywords: (entity, [entity_label_list])
		:return:
		'''
		entity_dict = {}
		for entity, types in keywords.items():
			for type in types:
				if type in entity_dict:
					entity_dict[type].append(entity)
				else:
					entity_dict[type] = [entity]
		return entity_dict

	def parser_main(self,question_classify_res):
		keywords = question_classify_res['keywords']
		entity_dict = self.extract_entity(keywords)

		question_type_list = question_classify_res['question_types']
		sql_list = []
		for question_type in question_type_list:
			sql = []
			if question_type == 'disease_symptom':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			elif question_type == 'symptom_disease':
				sql = self.sql_transfer(question_type,entity_dict.get('Symptom'))

			elif question_type == 'disease_cause':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_complication':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_avoid_food':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_good_food':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'food_avoid_disease':
				sql = self.sql_transfer(question_type,entity_dict.get('Food'))

			elif question_type == 'food_good_disease':
				sql = self.sql_transfer(question_type,entity_dict.get('Food'))

			elif question_type == 'disease_drug':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'drug_disease':
				sql = self.sql_transfer(question_type,entity_dict.get('Drug'))

			elif question_type == 'disease_check':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'check_disease':
				sql = self.sql_transfer(question_type,entity_dict.get('Check'))

			elif question_type == 'disease_prevent':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_treat_way':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_cure_prob':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_susceptible_people':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_department':
				sql = self.sql_transfer(question_type,entity_dict.get('Disease'))

			elif question_type == 'disease_treat_cost':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			elif question_type == 'disease_medical_insurance':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			elif question_type == 'disease_treat_cycle':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			elif question_type == 'disease_desc':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			elif question_type == 'disease_transmission_way':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			elif question_type == 'disease_nursing_way':
				sql = self.sql_transfer(question_type, entity_dict.get('Disease'))

			sql_dict = {}
			sql_dict['question_type'] = question_type
			if sql:
				sql_dict['sql'] = sql
				sql_list.append(sql_dict)
		return sql_list


	def sql_transfer(self,question_type,entities):
		if not entities:
			return []

		sql = []
		#TODO 1 已知疾病查询症状 disease_symptom
		if question_type == 'disease_symptom':
			sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' " \
				   "return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 2 已知症状判断疾病 symptom_disease
		elif question_type == 'symptom_disease':
			sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' " \
				   "return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 3 疾病原因 disease_cause
		elif question_type == 'disease_cause':
			sql = ["MATCH (m:Disease) where m.name = '{0}' " \
				   "return m.name, m.cause".format(i) for i in entities]

		#TODO 4 并发症 disease_complication
		elif question_type == 'disease_complication':
			sql = ["MATCH (m:Disease)-[r:has_complication]->(n:Disease) where m.name = '{0}' " \
				   "return m.name, r.name, n.name".format(i) for i in entities]
			# sql2 = [
			# 	"MATCH (m:Disease)-[r:has_complication]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(
			# 		i) for i in entities]
			# sql = sql1 + sql2

		#TODO 5 已知疾病查忌口食物 disease_avoid_food
		elif question_type == 'disease_avoid_food':
			sql = ["MATCH (m:Disease)-[r:avoid_food]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 已知疾病查推荐食物  disease_good_food
		elif question_type == 'disease_good_food':
			sql1 = ["MATCH (m:Disease)-[r:good_food]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
			sql2 = ["MATCH (m:Disease)-[r:recommand_recipes]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
			sql = sql1 + sql2

		#TODO 6 已知忌口食物查疾病 food_avoid_disease
		elif question_type == 'food_avoid_disease':
			sql = ["MATCH (m:Disease)-[r:avoid_food]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 7 已知推荐食物 查疾病 food_good_disease
		elif question_type == 'food_good_disease':
			sql1 = ["MATCH (m:Disease)-[r:good_food]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
			sql2 = ["MATCH (m:Disease)-[r:recommand_recipes]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
			sql = sql1 + sql2

		#TODO 7 疾病常用药品 disease_drug
		elif question_type == 'disease_drug':
			sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 8 药物治疗啥病 drug_disease
		elif question_type == 'drug_disease':
			sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 9 疾病检查项目 disease_check
		elif question_type == 'disease_check':
			sql = ["MATCH (m:Disease)-[r:check_item]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 10 已知检查项目查相应疾病 check_disease
		elif question_type == 'check_disease':
			sql = ["MATCH (m:Disease)-[r:check_item]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

		#TODO 11 疾病预防 disease_prevent
		elif question_type == 'disease_prevent':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

		#TODO 12 疾病治疗方法 disease_treat_way
		elif question_type == 'disease_treat_way':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treat_way".format(i) for i in entities]

		#TODO 13 疾病治愈可能性 disease_cure_prob
		elif question_type == 'disease_cure_prob':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_prob".format(i) for i in entities]

		#TODO 14 疾病易感人群 disease_susceptible_people
		elif question_type == 'disease_susceptible_people':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.susceptible_people".format(i) for i in entities]

		#TODO 15 疾病去哪个科室 disease_department
		elif question_type == 'disease_department':
			sql = ["MATCH (m:Disease)-[r:belongs_to]->(n:Department) where m.name = '{0}' return m.name,r.name,n.name".format(i) for i in entities]

		#TODO 16 疾病治疗费用 disease_treat_cost
		elif question_type == 'disease_treat_cost':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treat_cost".format(i) for i in entities]

		#TODO 17 疾病是否医保 disease_medical_insurance
		elif question_type == 'disease_medical_insurance':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.medical_insurance".format(i) for i in entities]

		#TODO 18 疾病治疗周期 disease_treat_cycle
		elif question_type == 'disease_treat_cycle':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treat_cycle".format(i) for i in entities]

		# TODO 19 疾病描述 disease_treat_cycle
		elif question_type == 'disease_desc':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

		# TODO 疾病传播方式
		elif question_type == 'disease_transmission_way':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.transmission_way".format(i) for i in entities]

		elif question_type == 'disease_nursing_way':
			sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.nursing".format(i) for i in entities]

		return sql