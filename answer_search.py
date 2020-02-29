# -*- coding:utf-8 -*-
# @Time : 2020/2/23 20:27
# @Author : TianWei
# @File : answer_search.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

from py2neo import Graph

class AnswerSearcher(object):
	def __init__(self):
		self.g = Graph(
			host="127.0.0.1",
			http_port=7474,
			user="neo4j",
			password="bravezhangw")
		self.num_limit = 20


	def search_main(self,sql_list):
		final_answers = []
		for sql_dict in sql_list:
			question_type = sql_dict['question_type']
			querys = sql_dict['sql']
			answers = []
			for query in querys:
				ress = self.g.run(query).data()
				answers += ress
			final_answer = self.answer_prettify(question_type,answers)
			if final_answer:
				final_answers.append(final_answer)
		return final_answers

	'''根据对应的qustion_type，调用相应的回复模板'''

	def answer_prettify(self, question_type, answers):
		final_answer = []
		if not answers:
			return ''
		if question_type == 'disease_symptom':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'symptom_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_cause':
			desc = [i['m.cause'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_prevent':
			desc = [i['m.prevent'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_treat_cycle':
			desc = [i['m.treat_cycle'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_treat_way':
			desc = [';'.join(i['m.treat_way']) for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_cure_prob':
			desc = [i['m.cure_prob'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_susceptible_people':
			desc = [i['m.susceptible_people'] for i in answers]
			subject = answers[0]['m.name']

			final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_desc':
			desc = [i['m.desc'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0},熟悉一下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_complication':
			desc = [i['n.name'] for i in answers]
			# desc2 = [i['m.name'] for i in answers]
			subject = answers[0]['m.name']
			# desc = [i for i in desc1 + desc2 if i != subject]
			final_answer = '{0}的并发症包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_avoid_food':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_good_food':
			do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
			recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
			subject = answers[0]['m.name']
			final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]),
																 ';'.join(list(set(recommand_desc))[:self.num_limit]))

		elif question_type == 'food_avoid_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

		elif question_type == 'food_good_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

		elif question_type == 'disease_drug':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'drug_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_check':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'check_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_department':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}所属科室为： {1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
		elif question_type == 'disease_treat_cost':
			desc = [i['m.treat_cost'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的治疗费用相关信息：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
		elif question_type == 'disease_medical_insurance':
			desc = [i['m.medical_insurance'] for i in answers]
			subject = answers[0]['m.name']
			if '是' in desc:
				final_answer = '{0}是医保疾病'.format(subject)
			else:
				pass
		elif question_type == 'disease_transmission_way':
			desc = [i['m.transmission_way'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的传播方式：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

		elif question_type == 'disease_nursing_way':
			desc = [i['m.nursing'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的护理方法：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


		return final_answer