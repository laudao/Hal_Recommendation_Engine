# -*- coding: utf-8 -*-
# filename : TopicGraph.py
# author : Laura NGUYEN
# creation date : 26/06/2017

from class_ModelLDA import ModelLDA
from class_PageHal import PageHAL
from GraphObjects import *
import pandas as pd
import os, re

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
			self.__nb_words = 5
	
	@ldamodel.setter
	def ldamodel(self, x):
		if not(self.page is None):
			model = ModelLDA(self.page, self.nb_topics, self.nb_passes, self.nb_words)
			f = open('topics/topic_language.txt', 'r')
			l = f.readline()
			if model.language != l:
				print("Can't create topics because languages are different")
				self.ldamodel = None
			else:
				f = open('topics/topic_num.txt', 'r')
				l = int(f.readline())
				print("ldamodel number " + str(l))
				ldamodel, doc_term_matrix, dic = model.extract_lda_topics()
				ldamodel.save('lda/lda.model' + str(l))
				f.close()
				self.__ldamodel = ldamodel
				l += 1
				f = open('topics/topic_num.txt', 'w')
				f.write(str(l))
				f.close()
		else:
			self.ldamodel = None

	@topics_list.setter
	def topics_list(self, x):
		if not(self.page is None) and not(self.ldamodel is None):
			self.__topics_list = self.ldamodel.show_topics(num_topics=self.nb_topics, num_words=self.nb_words,formatted=False)
		else:
			self.__topics_list = []
		
		if self.topics_list != []:
			print(self.topics_list)
			self.createGraph()


	def deleteRecommendations(self, graph):
		graph.run("MATCH ()-[r:RECOMMENDED_DOCS]->() DELETE r")
		graph.run("MATCH ()-[r:RECOMMENDED_AUTHORS]->() DELETE r")
		print("All previous recommendations have been deleted")

	def getNextId(self, graph):
		id_min = (pd.DataFrame((graph.run("MATCH (t:Topic) RETURN MAX(t.topic_id)")).data())).iloc[0]['MAX(t.topic_id)']
		
		""" no topic in database """
		if id_min == None:
			id_min = 0
		else:
			id_min = int(id_min) + 1
			
		print("Starting from id " + str(id_min))
		return id_min


	def createTopics(self, graph, t_id):
		""" create graph objects for each topic 
				topics_list = [(topic, [(word, weight)...])...] """
		for topic in self.topics_list:
			words = []
			weight = []
			""" topic[1] is a list of (word, weight) """
			for couple in topic[1]:
				words.append(couple[0])
				weight.append(couple[1])
			t = Topic(t_id, words, weight)
			graph.push(t)
			print("Topic " + str(t_id) + " created")
			t_id += 1


	def getListJaccardSim(self, l1, l2):
		l = []
		
		""" for each tuple in l1 """	
		for tuple1 in l1:
			w = tuple1[0]
			check = 0
			""" check if w is contained in a tuple in l2"""
			for tuple2 in l2:
				if w in tuple2:
					l.append([tuple1, tuple2])
					check = 1
			""" w is not in l2"""
			if check == 0:
				l.append([tuple1, (w, 0.0)])

		""" check for the remaining tuples in l2 and add them to l """
		for tuple2 in l2:
			w = tuple2[0]
			check = 1
			for couple in l:
				if w in couple[0]:
					check = 0
			if check == 1:
				l.append([tuple2, (w, 0.0)])
	
		return l

	def getJaccardSim(self, l1, l2):
		l = self.getListJaccardSim(l1, l2)

		inter=0
		union=0
		words_union = []
		weights_union = []

		""" Jaccard similarity """
		for couple in l:
			mini = min(couple[0][1], couple[1][1])
			inter += mini
			maxi = max(couple[0][1], couple[1][1])
			union += maxi
			weights_union.append(maxi)
			words_union.append(couple[0][0])

		sim = inter/union
		return sim, words_union, weights_union

	def mergeTopics(self, graph, t1, t2, weights_union, words_union, id_max, merging_info):	
		""" sort list according to words weight so that most relevant words are at the beginning """
		sorted_list = sorted(zip(weights_union, words_union), reverse=True)

		words = [word for (weight, word) in sorted_list]
		weights = [weight for (weight, word) in sorted_list]
		
		final_words = []
		final_weights = []
		""" keep most relevant (word, weight) """
		for i in range(self.nb_words):
			final_words.append(words[i])
			final_weights.append(weights[i])
		
		""" new topic id """
		t_id = id_max
		merging_info.append(id_max)
		id_max += 1

		""" create new topic """
		t = Topic(t_id, final_words, final_weights)	
		graph.push(t)

		merging_info[t1.topic_id] = t_id
		merging_info[t2.topic_id] = t_id 

		print("Merged topics " + str(t1.topic_id) + " and " + str(t2.topic_id) + " into topic " + str(t_id))

		""" delete topics 1 and 2 and their relationships """
		graph.run("MATCH (t:Topic)-[r:SIMILARITY]-() WHERE t.topic_id = " + str(t1.topic_id) + " DELETE r")
		graph.run("MATCH (t:Topic)-[r:SIMILARITY]-() WHERE t.topic_id = " + str(t2.topic_id) + " DELETE r")
		graph.run("MATCH (t: Topic)-[r:RELATED_TOPICS]-() WHERE t.topic_id = " + str(t1.topic_id) + " DELETE r")
		graph.run("MATCH (t: Topic)-[r:RELATED_TOPICS]-() WHERE t.topic_id = " + str(t2.topic_id) + " DELETE r")
		graph.run("MATCH (t:Topic) WHERE t.topic_id = " + str(t1.topic_id) + " DELETE t")
		graph.run("MATCH (t:Topic) WHERE t.topic_id = " + str(t2.topic_id) + " DELETE t")

		return id_max

	def createGraph(self):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")

		""" delete all topic-related relationships before pursuing """
		self.deleteRecommendations(graph)

		t_id = self.getNextId(graph)

		""" start_id.txt used to indicate, for each model, the limits of topic ids """
		if not(os.path.isfile("topics/start_id.txt")):
			f = open('topics/start_id.txt', 'w')
			f.write(str(t_id)+'\n')
			f.close()
		else:
			f = open('topics/start_id.txt', 'a')
			f.write(str(t_id)+'\n')
			f.close()

		id_max = t_id + self.nb_topics
		
		if not(os.path.isfile("topics/merging_info.txt")):
			""" t[i] : topic i merged into topic t[i] """
			merging_info = list(range(id_max))
			with open('topics/merging_info.txt', mode='wt', encoding='utf-8') as myfile:
 				myfile.write('\n'.join(str(i) for i in merging_info))
		else:
			with open('topics/merging_info.txt', 'r') as myfile:
				merging_info = myfile.read().splitlines()
			for i in range(len(merging_info)):
				merging_info[i] = int(merging_info[i])
			
			for i in range(t_id, id_max):
				merging_info.append(i)

		print(merging_info)
		self.createTopics(graph, t_id)


		""" for each topic, relate it to the other ones """
		for i in range(t_id, id_max):
			print("Current topic id: " + str(i))
			print(id_max)
			j=0
			t1 = Topic.select(graph, i).first()

			""" topic hasn't been deleted """
			if not(t1 is None):
				words1 = t1.sign_words
				weights1 = t1.words_prob
				l1 = []
	
				# contains tuples (word, weight) for each word in t1
				for word, weight in zip(words1, weights1):
					l1.append((word, weight))
				
				""" create relationships with other topics """
				while j != id_max:
					print("topic max : " + str(id_max))
					t2 = Topic.select(graph, j).first()

					""" topic hasn't been deleted """
					if not(t2 is None) and t1.topic_id != t2.topic_id:
						print("Linking topic " + str(t1.topic_id) + " and " + str(t2.topic_id))
						words2 = t2.sign_words
						weights2 = t2.words_prob
						l2 = []
						
						for word, weight in zip(words2, weights2):
							l2.append((word, weight))
						
						sim, words_union, weights_union = self.getJaccardSim(l1, l2)
							
						""" topics are too similar """
						if sim > 0.2:
							""" merge topics """
							id_max = self.mergeTopics(graph, t1, t2, weights_union, words_union, id_max, merging_info)
							break

						elif sim == 0:
							print("Topics " + str(t1.topic_id) + " and " + str(t2.topic_id) + " have nothing in common. No link added")
						else:
							""" add relationship between topics """
							t1.similar_topics.add(t2, kwproperties=sim)
							t2.similar_topics.add(t1, kwproperties=sim)
							print("Linked topics " + str(t1.topic_id) + " and " + str(t2.topic_id))
							graph.push(t2)
					elif t2 is None:
						print("Topic " + str(j) + " does not exist")

					graph.push(t1)
					j=j+1
		
		print(merging_info)
		with open('topics/merging_info.txt', mode='wt', encoding='utf-8') as myfile:
			myfile.write('\n'.join(str(i) for i in merging_info))
	
#page = PageHAL.create_page_file("rech.txt")
#tgr = TopicGraph(page, 100, 10, 10)

