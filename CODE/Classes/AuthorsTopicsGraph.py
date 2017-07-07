# -*- coding: utf-8 -*-
# filename : AuthorsTopicsGraph.py
# author : Laura NGUYEN
# creation date : 28/06/2017

from class_ModelLDA import ModelLDA
from class_PageHal import PageHAL
from GraphObjects import *
from AuthorsGraph import AuthorsGraph
from gensim import corpora, models
import numpy as np
import pandas as pd

class AuthorsTopicsGraph:
	def __init__(self, field, struct):
		self.field = field
		self.struct = struct
		self.authorsGraph = None
		self.authorsGraphCreated = None
		self.nb_topics = None
		self.nb_words = None
		self.ldamodel_list = None
		self.topics_list = None
		self.topic_language = None
#		self.topicsGraph = None

	@property
	def field(self):
		return self.__field

	@property
	def struct(self):
		return self.__struct

	@property
	def authorsGraph(self):
		return self.__authorsGraph

	@property
	def authorsGraphCreated(self):
		return self.__authorsGraphCreated

	@property
	def nb_topics(self):
		return self.__nb_topics

	@property
	def nb_words(self):
		return self.__nb_words

	@property
	def ldamodel_list(self):
		return self.__ldamodel_list

	@property
	def topics_list(self, x):
		return self.__topics_list

	@property
	def topic_language(self):
		return self.__topic_language

	@field.setter
	def field(self, x):
		self.__field = x

	@struct.setter
	def struct(self, x):
		self.__struct = x

	@authorsGraph.setter
	def authorsGraph(self, x):
		self.__authorsGraph = AuthorsGraph(self.field, self.struct)

	@authorsGraphCreated.setter
	def authorsGraphCreated(self, x):
		valid = self.authorsGraph.create_graph()
		if valid == True:
			self.__authorsGraphCreated = True
		else:
			self.__authorsGraphCreated = False

	@nb_topics.setter
	def nb_topics(self, x):
		f = open('topics_info.txt', 'r')
		self.__nb_topics = int((f.readline())[11:-1])
		f.close()

	@nb_words.setter
	def nb_words(self, x):
		f = open('topics_info.txt', 'r')
		f.readline()
		self.__nb_words = int((f.readline())[10:-1])
		f.close()

	@ldamodel_list.setter
	def ldamodel_list(self, x):
		f = open('topic_num.txt', 'r')
		l = int(f.readline())
		ldamodellist = []
		for i in range(l):
			ldamodellist.append(models.LdaModel.load('lda.model'+str(i)))
			print("Loaded ldamodel number " + str(i))
		self.__ldamodel_list = ldamodellist
		f.close()

	@topics_list.setter
	def topics_list(self, x):
		if not (self.ldamodel_list is None):
			topics_list = []
			for ldamodel in self.ldamodel_list:
				topics_list.append(ldamodel.show_topics(num_topics=self.nb_topics, num_words=self.nb_words,formatted=False))

	@topic_language.setter
	def topic_language(self, x):
		f = open('topic_language.txt', 'r')	
		l = f.readline()
		if l == 'en' or l == 'fr':
			self.__topic_language = l
	
	def get_valid_text(self, title, abstract, keywords):
		text = ""
		if PageHAL.string_is_valid(self.topic_language, title):
			text += title
		if (abstract != ""):
			if PageHAL.string_is_valid(self.topic_language, abstract):
				text += abstract
		if (keywords != ""):
			if PageHAL.string_is_valid(self.topic_language, keywords):
				text += keywords
		return text

	def getMostRelevantTopic(self, graph, text):
		max_topic = None
		max_weight = 0
		i=0
		print(text)
		""" search for the right topic in the right ldamodel """
		for ldamodel in self.ldamodel_list:
			print(i)
			i+=1
			updated = 0 
			split_text = text.split(' ')
			bow = ldamodel.id2word.doc2bow(split_text)
			doc_topics, word_topics, phi_values = ldamodel.get_document_topics(bow, per_word_topics=True)

			""" search for most relevant topic in current model """
			for tup in doc_topics:
				if tup[1] > max_weight:
					max_weight = tup[1]
					max_topic = tup[0]
					updated = 1
			
			""" get list of (topic_id, [(word, weight)...]) """
			topics_list = ldamodel.show_topics(num_topics=self.nb_topics, num_words=self.nb_words,formatted=False)
			
			""" most relevant topic among all models has changed since last iteration """
			if updated:
				""" search for the right topic id """
				for topic in topics_list:
					if max_topic == topic[0]:
						words = []
						for couple in topic[1]:
							words.append(couple[0])
						t = Topic.select(graph).where("_.sign_words = ['" + "','".join(words) + "']").first()
						
						""" topic was merged into another one """
						if t is None:
							print("topic " + str(max_topic) + " has been merged")
							with open('merging_info.txt', 'r') as myfile:
								merging_info = myfile.read().splitlines()
						
							for i in range(len(merging_info)):
								merging_info[i] = int(merging_info[i])
							
							""" search for right topic """
							while t is None:
								new_id = merging_info[max_topic]
								t = Topic.select(graph, new_id).first()
								max_topic = new_id
							
							print("Right topic is " + str(max_topic))
						else:
							max_topic = t.topic_id

		return max_topic, max_weight
		

	def link_doc_topics(self):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")

		""" get all articles """
		r = graph.run("MATCH (a:Article) RETURN a.docid")
		df = pd.DataFrame(r.data())

		""" for each article in the database """
		for row in df.itertuples():
			docid = int(row[1])
			doc = Article.select(graph, docid).first()
			
			""" check if article is already linked to a topic """
			link_exists = ((graph.run("MATCH (a:Article)-[r:RELATED_TOPICS]-(t:Topic) WHERE a.docid = " +str(docid) + " RETURN COUNT(r)")).data())[0]['COUNT(r)']

			""" article is not linked to any topic """
			if link_exists == 0:
				title = doc.title
				language = doc.language
				topic_id = None
				max_weight = 0

				if (language == self.topic_language):
					if doc.abstract == []:
						abstract = ""
					else:
						abstract = doc.abstract
					if doc.keywords == []:
						keywords = ""
					else:
						keywords = ' '.join(doc.keywords)
					print(type(keywords))
					print(abstract)
					text = self.get_valid_text(title, abstract, keywords)

					if text != "":
						topic_id, weight = self.getMostRelevantTopic(graph, text)
					
						topic = Topic.select(graph, topic_id).first()
						graph.run("MATCH (a:Article), (t:Topic) WHERE a.docid = " + str(docid) + " AND t.topic_id = " + str(topic_id) + " CREATE (a)-[r:RELATED_TOPICS {weight: " + str(weight) + "}]->(t)")
						graph.push(doc)
						graph.push(topic)
						print("topic " + str(topic_id) + " and doc " + str(docid) + " have been linked")
				else:
					print("Can't link " + str(docid) + " to any topic because languages are different")
			else:
				print("Article " + str(docid) + " is already linked to a topic")

	@staticmethod
	def createGraph():
		print("Do you want to search by the structure ... ")
		print(" 1 - id ?")
		print(" 2 - acronym?")
		print(" 3 - name?")

		print("Please select between the choices above")
		try:
			field = int(input("> "))
		except SyntaxError:
			field = None

		while field not in range(1, 4):
			field = int(input("Invalid input. Please select between the choices above\n> "))

		if field == 1:
			field = "id"
			struct = int(input("Enter the structure id\n> "))
		elif field == 2:
			field = "acronym"
			struct = input("Enter the structure acronym\n> ")
		else:
			field = "name"
			struct = input("Enter the structure name\n> ")

		while not(str(struct)) or (type(struct) != str and type(struct) != int):
			struct = input("Invalid input. Please enter a valid name/id/acronym\n> ")

		return AuthorsTopicsGraph(field, struct)

at = AuthorsTopicsGraph.createGraph()
print(at.authorsGraph.struct)
if (at.authorsGraphCreated == True):
	at.link_doc_topics()
else:
	print("Can't link topics and docs")
