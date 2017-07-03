# -*- coding: utf-8 -*-
# filename : AuthorsGraph.py
# author : Laura NGUYEN
# creation date : 21/06/2017
# provides a class to extract authors of a given structure

import pandas as pd
import numpy as np
import urllib as ur
import requests 
import json
import math
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

#	@authors.setter
#	def authors(self, x):
#		print("authors : " + str(x))
#		if (self.struct_type != 'unknown type'):
#			self.__authors = self.get_authors()
#		else:
#			self.__authors = 'unknown authors'

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
			url = "https://api.archives-ouvertes.fr/search/?q=structId_i:" + '"' + str(struct) + '"' + "&fl=docid authId_i authFullName_s authStructId_i abstract_s title_s producedDate_s keyword_s docType_s language_s"
			col = ['docid', 'authId_i', 'authFullName_s', 'authStructId_i', 'abstract_s','title_s', 'producedDate_s', 'keyword_s', 'docType_s', 'language_s', 'authQuality_s']					
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
	def create_single_struct(struct_type, struct_id, struct_name, struct_acro, struct_country):
		if struct_type == "researchteam":
			s = ResearchTeam(struct_id, struct_acro, struct_name, struct_country)
		elif struct_type == "department":
			s = Department(struct_id,struct_acro,struct_name,struct_country)
		elif struct_type == "laboratory":
			s = Laboratory(struct_id,struct_acro,struct_name,struct_country)
		else:
			s = Institution(struct_id,struct_acro,struct_name,struct_country)
		return s

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

		s = AuthorsGraph.create_single_struct(struct_type, struct_id, struct_name, struct_acro, struct_country)
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
	def link_parents(self, struct_id, child):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		
		df = AuthorsGraph.generate_DF(True, "id", struct_id)
		s_type = df.iloc[0]['type_s']
		s_acronym = df.iloc[0]['acronym_s']
		s_name = df.iloc[0]['name_s']
		s_country = df.iloc[0]['country_s']

		""" parents of structure struct_id """
		parent_id = df.iloc[0]['parentDocid_i'] 
		s = AuthorsGraph.create_single_struct(s_type, struct_id, s_name, s_acronym, s_country)
		graph.push(s)

		if child != None:
			s.children.add(child)
			child.is_part_of.add(s)
			graph.push(child)
			graph.push(s)

		#structure has no parents
#		if type(parent_id) != list:
#			return False
		# self.struct_id might be part of parent_id
#		elif str(self.struct_id) in parent_id: 
#			return True 
#		else:
		if struct_id != self.struct_id:
			if type(parent_id) == list:
				for parent in parent_id:
					self.link_parents(int(parent), s)
#				if check == True: 
#					return True
#			return False

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
			if (type(row[5]) == list):
				abstract = row[5][0]
			else:
				abstract = []
			title = row[6][0]
			pub_date = row[7]
			keywords = row[8]

			""" document doesn't have any keywords """
			if type(keywords) != list:
				keywords = []
			docType = row[9]
			lang = row[10][0]
			
			""" creates article """
			doc = Article(docid, title, abstract, keywords, docType, pub_date, lang)
			
			""" authors quality are unknown"""
			if type(row[11]) != list:
				list_qual = ["unknown"] * len(row[2])
			""" for each author having wrote the article """
			for a_id, auth, struct_id, qual in zip(row[2], row[3], row[4], list_qual):
				a = Author(auth_id=a_id, auth_name=auth, auth_quality=qual)
				df = AuthorsGraph.generate_DF(True, "id", struct_id)
				s_type = df.iloc[0]['type_s']
				s_acro = df.iloc[0]['acronym_s']
				s_name = df.iloc[0]['name_s']
				s_country = df.iloc[0]['country_s']

				s = AuthorsGraph.create_single_struct(s_type, struct_id, s_name, s_acro, s_country)
				""" link author and struc_id structure """
				a.belongs_to.add(s)
				s.members.add(a)

	#			""" author belongs to structure self.struct_id """
	#			if struct_id == self.struct_id and auth not in authors:
	#				authors.append(auth)
	#			else:
	#				""" author might belong in child structure of struct_id """
				self.link_parents(struct_id, None)
	#			authors.append(auth)
					
				doc.written_by.add(a)
				a.articles.add(doc)
				graph.push(a)
			
#			print(authors)
			graph.push(doc)
#		return authors

#authorsGraph = AuthorsGraph("id", 441569)
#print(authorsGraph.struct)
#print(authorsGraph.struct_id)
#print(authorsGraph.struct_type)
