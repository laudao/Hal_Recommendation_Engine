# -*- coding: utf-8 -*-
# filename : AuthorsGraph.py
# author : Laura NGUYEN
# creation date : 21/06/2017
# provides a class to extract authors of a given structure

import pandas as pd
import urllib as ur
import requests 
import json
from GraphObjects import *

class AuthorsGraph:
	def __init__(self, field, struct, struct_id=None, struct_type=None, authors=None):
		self.field = field
		self.struct = struct
		self.struct_id = struct_id
		self.struct_type = struct_type
#		self.authors = authors

	@property
	def field(self):
		return self.__field

	@property
	def struct(self):
		return self.__struct

	@property
	def struct_id(self):
		return self.__struct_id

	@property
	def struct_type(self):
		return self.__struct_type

#	@property
#	def authors(self):
#		return self.__authors

	@field.setter
	def field(self, x):
		self.__field = x

	@struct.setter
	def struct(self, x):
		print("struct : " + str(x))
		if not((type(x)==int and self.field=='id') or (type(x)==str and (self.field=='acronym' or self.field=='name'))):
			print("/!\ The fields haven't been filled in correctly /!\ ")
			print(str(x) + " is of type " + str(type(x)) + " but field is " + self.field)
			self.__struct = None
		else:
			self.__struct = x
			
	@struct_id.setter
	def struct_id(self, x):
		print("struct_id : " + str(x))
		if type(x) == int:
			self.__struct_id = x
		else:
			self.__struct_id = 'unknown id'

	@struct_type.setter
	def struct_type(self, x):
		print("struct_type : " +str(x))
		if not(self.struct is None):	
			self.__struct_type = self.findStructType()
		else:
			self.__struct_type = 'unknown type'

	def findStructType(self):
		df = AuthorsGraph.generate_DF(True, self.field, self.struct)
		if df.empty:
			print("Empty dataframe")
			return 'unknown type'
		else:
			struct_type = self.create_link_struct(df)
			return struct_type

	@staticmethod
	def generateURL(bool_struct, field, struct):
		# generates URL to collect data about structure
		if bool_struct == True:
			url = "https://api.archives-ouvertes.fr/ref/structure/?q=" 
			if field == "id":
				url = url + "docid"
			elif field == "acronym":
				url = url + "acronym_s" 
			else:
				url = url + "name_s"
			url = url +  ':"' + str(struct) + '"' + "&fl=docid acronym_s name_s country_s type_s parentDocid_i parentType_s"
			col = ['docid', 'acronym_s','name_s', 'country_s', 'type_s', 'parentDocid_i', 'parentType_s']
		# generates URL to collect data about authors of a structure
		else:
			url = "https://api.archives-ouvertes.fr/search/?q=structId_i:" + '"' + str(struct) + '"' + "&fl=docid authFullName_s authStructId_i abstract_s title_s producedDate_s keyword_s docType_s language_s authQuality_s&rows=50"
			col = ['docid', 'authFullName_s', 'authStructId_i', 'abstract_s','title_s', 'producedDate_s', 'keyword_s', 'docType_s', 'language_s', 'authQuality_s']					
		return url, col

	""" given a URL and column names, creates dataframe """
	@staticmethod
	def generate_DF(bool_struct, field, struct):
		url, col = AuthorsGraph.generateURL(bool_struct, field, struct)
		""" generates dataframe from URL """
		r = requests.get(url)
		dicjson = r.json()
		df = pd.DataFrame(dicjson['response']['docs'], columns=col).fillna(0)
		if df.empty:
			print("No data found")
		return df

	""" creates a structure """
	@staticmethod
	def create_single_struct(graph, struct_type, struct_id, struct_name, struct_acro, struct_country):
		""" used to indicate whether the structure was already created or not """
		existed = 1 		
		if struct_type == "researchteam":
			s = ResearchTeam.select(graph, struct_id).first()
			if s is None:
				existed = 0
				s = ResearchTeam(struct_id, struct_acro, struct_name, struct_country)
		elif struct_type == "department":
			s = Department.select(graph, struct_id).first()
			if s is None:
				existed = 0
				s = Department(struct_id,struct_acro,struct_name,struct_country)
		elif struct_type == "laboratory":
			s = Laboratory.select(graph, struct_id).first()
			if s is None:
				existed = 0
				s = Laboratory(struct_id,struct_acro,struct_name,struct_country)
		else:
			s = Institution.select(graph, struct_id).first()
			if s is None:
				existed = 0
				s = Institution(struct_id,struct_acro,struct_name,struct_country)
		return s, existed

	""" given a dataframe, creates a structure """
	def create_link_struct(self, df):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
	
		struct_type = df.iloc[0]['type_s']
		struct_id = int(df.reset_index().iloc[0]['docid'])
		struct_name = df.iloc[0]['name_s']
		struct_acro = df.iloc[0]['acronym_s']
		struct_parent_id = df.iloc[0]['parentDocid_i']
		struct_country = df.iloc[0]['parentType_s']
		struct_parent_type = df.iloc[0]['parentType_s']

		s, existed = AuthorsGraph.create_single_struct(graph, struct_type, struct_id, struct_name, struct_acro, struct_country)
		
		""" struct has just been created """
		if existed == 0:
			# self.struct is part of other structures
			if type(struct_parent_id) == list:
				for parent_id, parent_type in zip(struct_parent_id, struct_parent_type):
					if parent_type == "researchteam":
						parent = ResearchTeam.select(graph, int(parent_id)).first()
					elif parent_type == "department":
						parent = Department.select(graph, int(parent_id)).first()
					elif parent_type == "laboratory":
						parent = Laboratory.select(graph, int(parent_id)).first()
					elif parent_type == "institution":
						parent = Institution.select(graph, int(parent_id)).first()
					# links self.struct and its parents
					if parent != None:
						parent.children.add(s)
						s.is_part_of.add(parent)
		
			graph.push(s)

		self.struct_id = struct_id
		return struct_type

	""" given a structure, creates authors that belong to it """
	def create_graph(self):
		if not(self.struct is None) and self.struct_id != 'unknown id' and self.struct_type != 'unknown type':
			df = AuthorsGraph.generate_DF(False, "id", self.struct_id)
			self.create_authors_articles(df)
			return True
		else:
			print("Error: can't create graph")
			return False

	""" links author'structure with its parents """
	def link_parents(self, graph, struct_id, child):
		df = AuthorsGraph.generate_DF(True, "id", struct_id)
		s_type = df.iloc[0]['type_s']
		s_acronym = df.iloc[0]['acronym_s']
		s_name = df.iloc[0]['name_s']
		s_country = df.iloc[0]['country_s']

		""" parents of structure struct_id """
		parent_id = df.iloc[0]['parentDocid_i'] 
		s, existed = AuthorsGraph.create_single_struct(graph, s_type, struct_id, s_name, s_acronym, s_country)

		if existed == 0:
			graph.push(s)

		if child != None:
			s.children.add(child)
			child.is_part_of.add(s)
			print("  Linking " + str(s.struct_name) + " and " + str(child.struct_name))

		if struct_id != self.struct_id:
			if type(parent_id) == list:
				for parent in parent_id:
					self.link_parents(graph, int(parent), s)
		graph.push(s)

	""" creates authors, their articles and structures
	    links everything together
	"""
	def create_authors_articles(self, dataframe):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		
		""" for each row in the dataframe """
		for row in dataframe.itertuples():	
			docid = int(row[1])
			print(docid)
			doc = Article.select(graph, docid).first()

			""" doc already exists, no need to create it """
			if not(doc is None):	
				print("doc " + str(docid) + " already in database")
				continue

			""" document has abstract"""
			if (type(row[4]) == list):
				abstract = row[4][0]
			else:
				abstract = []
			title = row[5][0]
			pub_date = row[6]
			keywords = row[7]

			""" document doesn't have any keywords """
			if type(keywords) != list:
				keywords = []
			docType = row[8]
			lang = row[9][0]
			
			""" creates article """
			doc = Article(docid, title, abstract, keywords, docType, pub_date, lang)
			
			graph.push(doc)
			""" for each author of the article """
			for auth, struct_id, qual in zip(row[2], row[3], row[10]):
				a = Author.select(graph, auth).first()

				if not(a is None):
					print(a.auth_name + " already in database")
				else:	
					a = Author(auth)
					print(a.auth_name + " added to the database")
					graph.push(a)

				struct_id = int(struct_id)
				df = AuthorsGraph.generate_DF(True, "id", struct_id)
				s_type = df.iloc[0]['type_s']
				s_acro = df.iloc[0]['acronym_s']
				s_name = df.iloc[0]['name_s']
				s_country = df.iloc[0]['country_s']
					
				s, existed = AuthorsGraph.create_single_struct(graph, s_type, struct_id, s_name, s_acro, s_country)
				
				link_exists = ((graph.run('MATCH (a:Author)-[r:BELONGS_TO]->(s) WHERE a.auth_name = "' + a.auth_name + '" AND s.struct_id = ' + str(struct_id) + ' RETURN COUNT(r)')).data())[0]['COUNT(r)']
				""" structure has just been created """
				if existed == 0:
					self.link_parents(graph, struct_id, None)
				else:
					print(s_name + " already in the database")
				graph.push(a)	

				""" author was not linked to struct """
				if link_exists == 0:
					print("Added link between " + a.auth_name + " and " + s_name)
					a.belongs_to.add(s)
					s.members.add(a)
					graph.push(a)
				else:
					print(auth + " already linked to " + s_name)
				
				""" link author and article """
				graph.run('MATCH (a:Author), (d:Article) WHERE a.auth_name = "' + a.auth_name + '" AND d.docid = ' + str(docid) + ' CREATE (a)<-[w:WRITTEN_BY {quality: "' + qual + '"}]-(d)') 
				
			graph.push(doc)

#authorsGraph = AuthorsGraph("id", 408080)
#authorsGraph.create_graph()
#print(authorsGraph.struct)
#print(authorsGraph.struct_id)
#print(authorsGraph.struct_type)
