# -*- coding: utf-8 -*-
# filename : AuthorsTopicsGraph.py
# author : Laura NGUYEN
# creation date : 28/06/2017

from class_ModelLDA import ModelLDA
from class_PageHal import PageHAL
from GraphObjects import *
from AuthorsGraph import AuthorsGraph
from gensim import corpora, models

class AuthorsTopicsGraph:
	def __init__(self, field, struct):
		self.field = field
		self.struct = struct
		self.authorsGraph = None
		self.authorsGraphCreated = None
		self.ldamodel = None
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
	def ldamodel(self):
		return self.__ldamodel

	@property
	def topics_list(self, x):
		return self.__topics_list

	@property
	def topic_language(self):
		return self.__topic_language

#	@property
#	def topicsGraph(self):
#		return self.__topicsGraph

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

	@ldamodel.setter
	def ldamodel(self, x):
		self.__ldamodel = models.LdaModel.load('lda.model')

	@topics_list.setter
	def topics_list(self, x):
		if not (self.ldamodel is None):
			self.__topics_list = self.ldamodel.show_topics(formatted=False)
		
	@topic_language.setter
	def topic_language(self, x):
		f = open('topic_language.txt', 'r')	
		l = f.readline()
		if l == 'en' or l == 'fr':
			self.__topic_language = l
		
#	@topicsGraph.setter
#	def topicsGraph(self, x):
#		filename = "rech.txt"
#		page = PageHAL.create_page_file(filename)
#		self.__topicsGraph = TopicGraph(page, 100, 10, 5)
#		self.topicsGraph.create_link_TopicGraph()

	def link_doc_topics(self):
		df = AuthorsGraph.generate_DF(False, "id", self.authorsGraph.struct_id)
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")

		for row in df.itertuples():
			docid = int(row[1])
			doc = Article.select(graph, docid).first()

			if doc is None:
				print("Article " + string(id) + " not added to the database yet")
			else:
				title = doc.title
				language = row[10][0]

				if (language == self.topic_language):
					abstract = ' '.join(doc.abstract)
					keywords = ' '.join(doc.keywords)
					text = ""

					if PageHAL.string_is_valid(self.topic_language, title):
						text += title
					if (abstract != ""):
						if PageHAL.string_is_valid(self.topic_language, abstract):
							text += abstract
					if (keywords != ""):
						if PageHAL.string_is_valid(self.topic_language, keywords):
							text += keywords
				
					if text != "":
						text = text.split(' ')
						bow = self.ldamodel.id2word.doc2bow(text)
						doc_topics, word_topics, phi_values = self.ldamodel.get_document_topics(bow, per_word_topics=True)
						max_value = (0,0)
						for tuple in doc_topics:
							if tuple[1] > max_value[1]:
								max_value = tuple
	
						rel_topic = max_value[0]

						topic = Topic.select(graph, rel_topic).first()
						doc.related_topics.add(topic, kwproperties=max_value[1])
						topic.related_articles.add(doc)
						graph.push(doc)
						graph.push(topic)
				else:
					print("Can't link article " + str(docid) + " and topics because language is different")	

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
			field = input("Invalid input. Please select between the choices above\n> ")

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


