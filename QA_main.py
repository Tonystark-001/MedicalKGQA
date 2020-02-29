# -*- coding:utf-8 -*-
# @Time : 2020/2/23 20:33
# @Author : TianWei
# @File : QA_main.py
# @Software: PyCharm
# @Organization : NJU
# @email : cleverzhangw@qq.com

from answer_search import *
from question_classification import *
from question_parser import *
import dill #序列号objedt

class QuestionAnswerSystem(object):
	def __init__(self):
		self.classifier = QuestionClassifier()
		self.question_parser = QuestionParser()
		self.answer_searcher = AnswerSearcher()

	def question_answer_main(self,question):
		answer = "非常抱歉，这个问题超出小医的能力范围！"
		classify_res = self.classifier.classify_main(question)
		print(classify_res)
		if not classify_res: # 无法解析问句
			return answer

		res_sql = self.question_parser.parser_main(classify_res)
		print(res_sql)
		final_answers = self.answer_searcher.search_main(res_sql)

		if not final_answers:
			return answer
		else:
			return '\n'.join(final_answers)

if __name__ == '__main__':
	handler = QuestionAnswerSystem()
	while True:
		question = input("用户:")
		answer = handler.question_answer_main(question)
		print(answer)

