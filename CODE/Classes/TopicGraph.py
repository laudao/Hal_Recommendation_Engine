# -*- coding: utf-8 -*-
# filename : TopicGraph.py
# author : Laura NGUYEN
# creation date : 26/06/2017

from class_ModelLDA import ModelLDA
from class_PageHal import PageHAL
from GraphObjects import *

class TopicGraph:
	def __init__(self, page, nb_passes, nb_topics, nb_words):
		self.page = page
		self.nb_passes = nb_passes
		self.nb_topics = nb_topics
		self.nb_words = nb_words
		self.ldamodel = None
		self.topics_list = []

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
	def ldamodel(self):
		return self.__ldamodel

	@property
	def topics_list(self):
		return self.__topics_list

	@page.setter
	def page(self, x):
		if type(x) == PageHAL:
			self.__page = x
#			try:
#				self.ModelLDA = "ok"
#			except AttributeError:
#				pass
		else:
			print("type of ", x, " must be PageHAL")
			self.__page = None
	
	@nb_passes.setter
	def nb_passes(self, x):
		if type(x) == int and x > 0:
			self.__nb_passes = x
		else:
			print("nb_passes must be a positive integer")
			print("default value of nb_passes is 50")
			self.__nb_passes = 50

	@nb_topics.setter
	def nb_topics(self, x):
		if type(x) == int and x > 0:
			self.__nb_topics = x
		else:
			print("nb_topics must be a positive integer")
			print("default value of nb_topics is 5")
			self.__nb_topics = 5

	@nb_words.setter
	def nb_words(self, x):
		if type(x) == int and x > 0:
			self.__nb_words = x
		else:
			print("nb_words must be a positive integer")
			print("default value of nb_words is 5")
	
	@ldamodel.setter
	def ldamodel(self, x):
		if not(self.page is None):
			model = ModelLDA(self.page, self.nb_topics, self.nb_passes, self.nb_words)
			ldamodel, doc_term_matrix, dic = model.extract_lda_topics()
			ldamodel.save('lda.model')
			self.__ldamodel = ldamodel
		else:
			self.ldamodel = None

	@topics_list.setter
	def topics_list(self, x):
		if not(self.page is None):
			self.__topics_list = self.ldamodel.show_topics(formatted=False)
#			f = open('topics_list.txt', 'w')
#			for tuple in topics_list:
#				f.write(' '.join(str(s) for s in tuple) + '\n')
		else:
			self.__topics_list = []
	
	def create_link_TopicGraph(self):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")

		""" delete all topic objects before pursuing """
		graph.data("MATCH (n:Topic) OPTIONAL MATCH (n)-[r]-() DELETE r, n")

		""" create graph objects for each topic 
				topics_list = [(topic, [(word, weight)...])...] """
		for topic in self.topics_list:
			words = []
			weight = []
			""" topic[1] is a list of (word, weight) """
			for couple in topic[1]:
				words.append(couple[0])
				weight.append(couple[1])
			t = Topic(topic[0], words, weight)
			graph.push(t)
			print("Topic " + str(topic[0]) + " created")

		""" for each topic, relate it to the other ones """
		for i in range(self.nb_topics):
			j=i+1
			t1 = Topic.select(graph, i).first()
			words1 = t1.sign_words
			weights1 = t1.words_prob
			l1 = []

			# contains tuples (word, weight) for each word in t1
			for word, weight in zip(words1, weights1):
				l1.append((word, weight))
			
			while j != self.nb_topics:
				t2 = Topic.select(graph, j).first()
				words2 = t2.sign_words
				weights2 = t2.words_prob
				l2 = []
				
				for word, weight in zip(words2, weights2):
					l2.append((word, weight))

				all = []
				if (len(l1) > len(l2)):
					list1 = l1
					list2 = l2
				else:
					list1 = l2
					list2 = l1

				""" for each tuple"""	
				for tuple1 in list1:
					w = tuple1[0]
					check = 0
					""" check if w is contained in a tuple in list2"""
					for tuple2 in list2:
						if w in tuple2:
							all.append([tuple1, tuple2])
							check = 1
					""" w is not in list2"""
					if check == 0:
						all.append([tuple1, (w, 0.0)])

				inter=0
				union=0
				""" Jaccard similarity """
				for couple in all:
					print(couple)
					mini = min(couple[0][1], couple[1][1])
					inter = inter + mini
					maxi = max(couple[0][1], couple[1][1])
					union = union + maxi
				sim = inter/union
				print("inter : " + str(inter))
				print("union : " + str(union))
			#	if sim > 0.6:
			#		# delete t2
			#		pass 
			#	else:
				""" add relationship between topics """
				print("sim : " + str(sim))
				t1.similar_topics.add(t2, kwproperties=sim)
				t2.similar_topics.add(t1, kwproperties=sim)
				graph.push(t1)
				graph.push(t2)
				j=j+1
			
page = PageHAL.create_page_file("rech.txt")
tgr = TopicGraph(page, 100, 5, 10)
tgr.create_link_TopicGraph()

