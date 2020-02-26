# -*- coding:utf-8 -*-
# @Time : 2020/2/22 19:48
# @Author : TianWei
# @File : build_medical_graph.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

import os
import json
from py2neo import Graph, Node, Relationship
import utils
import logging
class MedicalGraph(object):
	def __init__(self):
		self.cur_dir = "/".join(os.path.abspath(__file__).split("/")[:-1])
		self.data_path = os.path.join(self.cur_dir, 'data/medical.json')
		self.log_path = os.path.join(self.cur_dir, 'log/build_medical.txt')
		self.g = Graph(
			host="127.0.0.1",
			http_port=7474,
			user="neo4j",
			password="bravezhangw"
		)

	def delete_exist_graph(self):
		self.g.delete_all()
		logging.info(" - graph delete finished.")

	def load_json(self, file_path):
		with open(file_path, "r", encoding='utf-8') as f:
			data = json.load(f)
		return data

	def read_nodes(self):
		# TODO 共 6 类节点
		unique_diseases = []  # 疾病
		unique_symptoms = []  # 疾病症状
		unique_departments = []  # 所属科室
		unique_checks = []  # 检查项目
		unique_drugs = []  # 药品
		unique_foods = []  # 食物

		diseases_info = []  # 疾病综合信息列表

		# TODO 构建实体间的关系
		rels_depart_depart = []  # 科室——科室
		rels_disease_eat = []  # 疾病——宜吃食物
		rels_disease_no_eat = []  # 疾病——忌口食物
		rels_disease_recipes = []  # 疾病——推荐食谱
		rels_disease_drug = []  # 疾病——常用药物
		rels_disease_check = []  # 疾病——检查项目
		rels_disease_symptom = []  # 疾病——症状
		rels_disease_complication = []  # 疾病——并发症
		rels_disease_department = []  # 疾病——所属科室

		count = 0
		all_data = self.load_json(self.data_path)  # {index, item} item是单个疾病各种信息组成的json语句
		# TODO 每一次获取一种疾病特征并加入列表
		for ind, item in all_data.items():
			disease_dict = {}
			gaishu_info = item['gaishu_info']
			cause_info = item['cause_info']
			prevent_info = item['prevent_info']
			symptom_info = item['symptom_data']
			inspect_info = item['inspect_info']
			nursing_info = item['nursing_info']
			food_info = item['food_info']

			disease_dict['name'] = ''
			disease_dict['desc'] = ''
			disease_dict['medical_insurance'] = ''
			disease_dict['disease_ratio'] = ''
			disease_dict['susceptible_people'] = ''
			disease_dict['transmission_way'] = ''
			disease_dict['has_complication'] = ''
			disease_dict['belongs_to_department'] = ''
			disease_dict['treat_way'] = ''
			disease_dict['treat_cycle'] = ''
			disease_dict['cure_prob'] = ''
			disease_dict['common_drug'] = ''
			disease_dict['treat_cost'] = ''
			disease_dict['nursing'] = ''
			disease_dict['cause'] = ''
			disease_dict['prevent'] = ''

			# 疾病名称
			if 'name' in gaishu_info:
				disease_dict['name'] = gaishu_info['name']
				disease_name = gaishu_info['name']
			else:
				print("此疾病名字丢失，跳过。")
				continue

			unique_diseases.append(disease_name)  # 添加新的疾病类别

			# 疾病描述
			if 'desc' in gaishu_info:
				disease_dict['desc'] = gaishu_info['desc']

			# 是否医保疾病
			if 'medical_insurance' in gaishu_info:
				disease_dict['medical_insurance'] = gaishu_info['medical_insurance']

			# 患病比例
			if 'disease_ratio' in gaishu_info:
				disease_dict['disease_ratio'] = gaishu_info['disease_ratio']

			# 易感人群
			if 'susceptible_people' in gaishu_info:
				disease_dict['susceptible_people'] = gaishu_info['susceptible_people']

			# 传染性 或 传染方式
			if 'transmission_way' in gaishu_info:
				disease_dict['transmission_way'] = gaishu_info['transmission_way']

			# 并发症
			if 'has_complication' in gaishu_info:
				if gaishu_info['has_complication']:
					complications = gaishu_info['has_complication']
					for complication in complications:
						if complication.strip():
							rels_disease_complication.append([disease_name, complication])

					# unique_diseases += complications
			# 所属科室
			'''
				科室可能为1个或2个
				1个就是疾病与科室关系
				2个多出科室与科室的关系
			'''
			if 'belongs_to_department' in gaishu_info: # (eg . ['内科  风湿免疫科'])
				if gaishu_info['belongs_to_department']:
					departments = gaishu_info['belongs_to_department']
					if len(departments) == 1:
						if departments[0].strip():
							rels_disease_department.append([disease_name, departments[0]])
					else:
						big = departments[0].strip()
						small = departments[1].strip()
						if big.strip():
							rels_disease_department.append([disease_name, big])
						if small.strip():
							rels_depart_depart.append([small, big])
					# disease_dict['belongs_to_department'] = gaishu_info['belongs_to_department']

					unique_departments += departments

			# 治疗方式
			if 'treat_way' in gaishu_info:
				if gaishu_info['treat_way']:
					disease_dict['treat_way'] = gaishu_info['treat_way']
				else:
					disease_dict['treat_way'] = []

			# 治疗周期
			if 'treat_cycle' in gaishu_info:
				disease_dict['treat_cycle'] = gaishu_info['treat_cycle']

			# 治愈可能性质
			if 'cure_prob' in gaishu_info:
				disease_dict['cure_prob'] = gaishu_info['cure_prob']

			# 常用药物
			if 'common_drug' in gaishu_info:
				if gaishu_info['common_drug']:
					drugs = gaishu_info['common_drug']
					for drug in drugs:
						if drug.strip():
							rels_disease_drug.append([disease_name, drug])
					unique_drugs += drugs
			# disease_dict['common_drug'] = gaishu_info['common_drug']

			# 治疗费用
			if 'treat_cost' in gaishu_info:
				disease_dict['treat_cost'] = gaishu_info['treat_cost']

			# 疾病原因
			if cause_info:
				disease_dict['cause'] = cause_info

			# 预防方法
			if prevent_info:
				disease_dict['prevent'] = prevent_info

			# 护理方法
			if nursing_info:
				disease_dict['nursing'] = nursing_info

			# 疾病症状
			if 'symptoms' in symptom_info:
				for symptom in symptom_info['symptoms']:
					if symptom.strip():
						rels_disease_symptom.append([disease_name, symptom])
				unique_symptoms += symptom_info['symptoms']

			# 宜吃食物
			if 'good_food' in food_info:
				for food in food_info['good_food']:
					if food.strip():
						rels_disease_eat.append([disease_name, food])
				unique_foods += food_info['good_food']

			# 忌吃食物
			if 'avoid_food' in food_info:
				for food in food_info['avoid_food']:
					if food.strip():
						rels_disease_no_eat.append([disease_name, food])
				unique_foods += food_info['avoid_food']

			# 推荐食谱
			if 'recommand_recipes' in food_info:
				for recipes in food_info['recommand_recipes']:
					if recipes.strip():
						rels_disease_recipes.append([disease_name, recipes])
				unique_foods += food_info['recommand_recipes']

			# 检查项目
			if inspect_info:
				for check in inspect_info:
					if check.strip():
						rels_disease_check.append([disease_name, check])
				unique_checks += inspect_info

			count += 1
			diseases_info.append(disease_dict)  # 把整理好的疾病信息加入列表

		return set(unique_diseases), set(unique_symptoms), set(unique_departments), \
			   set(unique_checks), set(unique_drugs), set(unique_foods), diseases_info, rels_depart_depart, \
			   rels_disease_eat, rels_disease_no_eat, rels_disease_recipes, rels_disease_drug, rels_disease_check, \
			   rels_disease_symptom, rels_disease_complication, rels_disease_department

	'''导出数据'''

	def export_data(self):
		Diseases, Symptoms, Departments, \
		Checks, Drugs, Foods, \
		diseases_info, \
		rels_depart_depart, rels_disease_eat, rels_disease_no_eat, rels_disease_recipes, rels_disease_drug, \
		rels_disease_check, rels_disease_symptom, rels_disease_complication, rels_disease_department = self.read_nodes()
		f_drug = open('./region_words/drugs.txt', 'w+',encoding='utf-8')
		f_food = open('./region_words/foods.txt', 'w+',encoding='utf-8')
		f_check = open('./region_words/checks.txt', 'w+',encoding='utf-8')
		f_department = open('./region_words/departments.txt', 'w+',encoding='utf-8')
		f_symptom = open('./region_words/symptoms.txt', 'w+',encoding='utf-8')
		f_disease = open('./region_words/diseases.txt', 'w+',encoding='utf-8')

		f_drug.write('\n'.join(list(Drugs)))
		f_food.write('\n'.join(list(Foods)))
		f_check.write('\n'.join(list(Checks)))
		f_department.write('\n'.join(list(Departments)))
		f_symptom.write('\n'.join(list(Symptoms)))
		f_disease.write('\n'.join(list(Diseases)))

		f_drug.close()
		f_food.close()
		f_check.close()
		f_department.close()
		f_symptom.close()
		f_disease.close()
		return

	# 创建中心节点（疾病为中心节点）
	def create_disease_nodes(self,diseases_info):
		logging.info(" - {} nodes".format("Disease"))
		count = 0
		for disease_dict in diseases_info:
			node = Node("Disease",
						name=disease_dict['name'],
						desc=disease_dict['desc'],
						medical_insurance=disease_dict['medical_insurance'],
						disease_ratio=disease_dict['disease_ratio'],
						disease_dict=disease_dict['susceptible_people'],
						transmission_way=disease_dict['transmission_way'],
						treat_way=disease_dict['treat_way'],
						treat_cycle=disease_dict['treat_cycle'],
						cure_prob=disease_dict['cure_prob'],
						treat_cost=disease_dict['treat_cost'],
						nursing=disease_dict['nursing'],
						cause=disease_dict['cause'],
						prevent=disease_dict['prevent']
						)
			self.g.create(node)
			count += 1
		logging.info(" - Disease count : {}".format(count))
		return

	def create_general_nodes(self,label,node_names):
		'''
		创建一般节点
		:param label:
		:param node_names:
		:return:
		'''
		logging.info(" - {} nodes".format(label))
		count = 0
		for name in node_names:
			node = Node(label,name=name)
			self.g.create(node)
			count += 1
		logging.info(" - {} count : {}".format(label,count))

	def create_graph_nodes(self):
		Diseases, Symptoms, Departments, \
		Checks, Drugs, Foods, \
		diseases_info, \
		rels_depart_depart, rels_disease_eat, rels_disease_no_eat, rels_disease_recipes, rels_disease_drug, \
		rels_disease_check, rels_disease_symptom, rels_disease_complication, rels_disease_department = self.read_nodes()
		self.create_disease_nodes(diseases_info)
		self.create_general_nodes("Symptom",Symptoms)
		self.create_general_nodes("Department",Departments)
		self.create_general_nodes("Check",Checks)
		self.create_general_nodes("Drug",Drugs)
		self.create_general_nodes("Food",Foods)

	rels_depart_depart = []  # 科室——科室
	rels_disease_eat = []  # 疾病——宜吃食物
	rels_disease_no_eat = []  # 疾病——忌口食物
	rels_disease_recipes = []  # 疾病——推荐食谱
	rels_disease_drug = []  # 疾病——常用药物
	rels_disease_check = []  # 疾病——检查项目
	rels_disease_symptom = []  # 疾病——症状
	rels_disease_complication = []  # 疾病——并发症
	rels_disease_department = []  # 疾病——所属科室

	def create_graph_rels(self):
		Diseases, Symptoms, Departments, \
		Checks, Drugs, Foods, \
		diseases_info, \
		rels_depart_depart, rels_disease_eat, rels_disease_no_eat, rels_disease_recipes, rels_disease_drug, \
		rels_disease_check, rels_disease_symptom, rels_disease_complication, rels_disease_department = self.read_nodes()
		self.create_relationship("Department","Department",rels_depart_depart,"belongs_to","属于")
		self.create_relationship("Disease","Food",rels_disease_eat,"good_food","宜吃食物")
		self.create_relationship("Disease","Food",rels_disease_no_eat,"avoid_food","忌吃食物")
		self.create_relationship("Disease","Food",rels_disease_recipes,"recommand_recipes","推荐食谱")
		self.create_relationship("Disease","Drug",rels_disease_drug,"common_drug","常用药物")
		self.create_relationship("Disease","Check",rels_disease_check,"check_item","检查项目")
		self.create_relationship("Disease","Symptom",rels_disease_symptom,"has_symptom","疾病症状")
		self.create_relationship("Disease","Disease",rels_disease_complication,"has_complication","并发症")
		self.create_relationship("Disease","Department",rels_disease_department,"belongs_to","所属科室")

	def create_relationship(self,start_node,end_node,edges,rel_type,rel_name):
		count = 0
		set_edges = []
		for edge in edges:
			set_edges.append("$$".join(edge))
		unique_edges = set(set_edges)
		num_relations = len(unique_edges)
		logging.info(" - {} ---- {}".format(start_node,end_node))
		logging.info(" - rel_type: {}".format(rel_type))
		logging.info(" - Original relations number : {}".format(num_relations))
		for edge in unique_edges:
			edge = edge.split("$$")
			p = edge[0]
			q = edge[1]
			query = 'match(p:%s),(q:%s) where p.name="%s" and q.name="%s" create (p)-[rel:%s{name:"%s"}]->(q)' % \
				(start_node,end_node,p,q,rel_type,rel_name)
			try:
				self.g.run(query)
				count += 1
			except Exception as e:
				logging.info(e)
		logging.info(" - {} relations have been created successfully.".format(count))
		return

if __name__ == '__main__':
	handler = MedicalGraph()
	# utils.set_logger(handler.log_path)
	# handler.delete_exist_graph()
	# handler.create_graph_nodes()
	# handler.create_graph_rels()
	# handler.export_data()
