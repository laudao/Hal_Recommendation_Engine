# -*- coding: utf-8 -*-
# filename : TopicGraph.py
# author : Laura NGUYEN
# creation date : 26/06/2017

from class_ModelLDA import ModelLDA
from GraphObjects import *

class TopicGraph:
	def __init__(self, page, nb_passes, nb_topics, nb_words):
		self.page = page
		self.nb_passes = nb_passes
		self.nb_topics = nb_topics
		self.nb_words = nb_words
		self.topics_list = 'unknown'

	@property
	def page(self):
		return self.__page

	@property
	def nb_passes(self):
		return self.__nb_passes

	@property
	def nb_topics(self):
		return self.__nb_topics

	@property
	def nb_words(self):
		return self.__nb_words

	@property
	def topics_list(self):
		return self.__topics_list

	@page.setter
	def page(self, x):
		if type(x) == PageHAL:
			self.__page = x
			try:
				self.ModelLDA = "ok"
			except AttributeError:
				pass
		else:
			print("type of ", x, " must be PageHAL")
	
	@nb_passes.setter
	def nb_passes(self, x):
		if type(x) == int and x > 0:
			self.__nb_passes = x
		else:
			print("nb_passes must be a positive integer")

	@nb_topics.setter
	def nb_topics(self, x):
		if type(x) == int and x > 0:
			self.__nb_topics = x
		else:
			print("nb_topics must be a positive integer")

	@nb_words.setter
	def nb_words(self, x):
		if type(x) == int and x > 0:
			self.__nb_words = x
		else:
			print("nb_words must be a positive integer")
	
	@topics_list.setter
	def topics_list(self, x):
		if x == "ok":
			model = ModelLDA(self.page, self.nb_topics, self.nb_passes, self.nb_words)
			ldamodel, doc_term_matrix, dic = model.extract_lda_topics()
			self.__topics_list = ldamodel.show_topics(formatted=False)
	
	def create_link_TopicGraaph(self):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		for topic in self.topics_list:
			words = []
			weight = []
			for couple in topic[1]:
				words.append(couple[0])
				weight.append(couple[1])
			t = Topic(topic[0], words, weight)
			graph.push(t)

		for i in range(self.nb_topics):
			j=i+1
			t1 = Topic.select(graph, i).first()
			words1 = t1.sign_words
			weights1 = t1.words_prob

			while j != self.nb_topics:
				t2 = Topic.select(graph, j).first()
				words2 = t2.sign_words
				weights2 = t2.words_prob


page = PageHAL.create_page_file("rech.txt")
tgr = TopicGraph(page, 60, 8, 10)

