# -*- coding: utf-8 -*-
# filename : searchAuthors.py
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

class SearchAuthors:
	def __init__(self, field, struct):
		self.field = field
		self.struct = struct
		self.struct_id = None
		self.struct_type = "unknown"
		self.authors = "unknown"

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

	@property
	def authors(self):
		return self.__authors

	@field.setter
	def field(self, x):
		self.__field = x

	@struct.setter
	def struct(self, x):
		self.__struct = x

		if not((type(x)==int and self.field=='id') or (type(x)==str and (self.field=='acronym') or (self.field=='name'))):
			print("The fields haven't been filled in correctly.")
			try:
				self.struct_type = 'error'
			except AttributeError:
				pass
		else:
			self.struct_type = "go"
			
	@struct_id.setter
	def struct_id(self, x):
		print("ici")
		self.__struct_id = x

	@struct_type.setter
	def struct_type(self, x):
		if x == "go":
			self.__struct_type = self.findStructType()
			if self.struct_type != "error":
				try:
					self.authors = "ok"
				except AttributeError:
					pass
		else:
			pass

	@authors.setter
	def authors(self, x):
		if x == "ok":
			self.__authors = self.get_authors()
		elif x == "ko":
			print("Can't find authors")
		else:
			pass

	def findStructType(self):
		df = SearchAuthors.generate_DF(True, self.field, self.struct)
		if df.empty:
			return "error"
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
		url, col = SearchAuthors.generateURL(bool_struct, field, struct)
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
			s = ResearchTeam(rteam_id=struct_id, rteam_name=struct_name,rteam_acronym = struct_acro,rteam_country=struct_country)
		elif struct_type == "department":
			s = Department(dept_id=struct_id,dept_name=struct_name,dept_acronym=struct_acro,dept_country=struct_country)
		elif struct_type == "laboratory":
			s = Laboratory(lab_id=struct_id,lab_name=struct_name,lab_acronym=struct_acro,lab_country=struct_country)
		else:
			s = Institution(inst_id=struct_id,inst_name=struct_name,inst_acronym=struct_acro,inst_country=struct_country)
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

		s = SearchAuthors.create_single_struct(struct_type, struct_id, struct_name, struct_acro, struct_country)
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
		self.__struct_id = struct_id
		return struct_type

	""" given a structure, creates authors that belong to it """
	def get_authors(self):
		df = SearchAuthors.generate_DF(False, "id", self.struct_id)
		authors = self.create_authors_articles(df)
		return authors

	""" looks for self.struct_id in parents of struct_id 
			returns true if author's struct is part of struct_id
			returns false otherwise 
	"""
	def check_parents(self, struct_id, child):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		
		df = SearchAuthors.generate_DF(True, "id", struct_id)
		s_type = df.iloc[0]['type_s']
		s_acronym = df.iloc[0]['acronym_s']
		s_name = df.iloc[0]['name_s']
		s_country = df.iloc[0]['country_s']

		parent_id = df.iloc[0]['parentDocid_i']
		
		s = SearchAuthors.create_single_struct(s_type, struct_id, s_name, s_acronym, s_country)
		graph.push(s)

		if child != None:
			s.children.add(child)
			child.is_part_of.add(s)
			graph.push(child)

		#structure has no parents
		if type(parent_id) != list:
			return False
		# self.struct_id might be one of parents
		elif self.struct_id in parent_id: 
			return True 
		else:
			# look for self.struct_id in parents of parent structures
			for parent in parent_id:
				check = self.check_parents(parent, s)
				if check == True: 
					return True
			return False

	""" creates authors, their articles and structures
	    links everything 
	"""
	def create_authors_articles(self, dataframe):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		authors = []
		i=0
		""" for each row in the dataframe """
		for row in dataframe.itertuples():	
			docid = int(row[1])
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
		
			if type(row[11]) != list:
				list_qual = ["unknown"] * len(row[2])
			""" for each author having wrote the article """
			for a_id, auth, struct_id, qual in zip(row[2], row[3], row[4], list_qual):
				a = Author(auth_id=a_id, auth_name=auth, auth_quality=qual)
				df = SearchAuthors.generate_DF(True, "id", struct_id)
				s_type = df.iloc[0]['type_s']
				s_acro = df.iloc[0]['acronym_s']
				s_name = df.iloc[0]['name_s']
				s_country = df.iloc[0]['country_s']

				s = SearchAuthors.create_single_struct(s_type, struct_id, s_name, s_acro, s_country)
				a.belongs_in.add(s)
				s.members.add(a)

				""" author belongs in structure self.struct_id """
				if struct_id == self.struct_id and auth not in authors:
					authors.append(auth)
				else:
					""" author might belong in child structure of struct_id """
					if (self.check_parents(struct_id, None) and auth not in authors):
						authors.append(auth)
					
				doc.written_by.add(a)
				a.article.add(doc)
				graph.push(a)
				print(authors)

			graph.push(doc)

		return authors

search = SearchAuthors("acronym", "IDH")
print(search.struct)
print(search.struct_id)
print(search.struct_type)
print(search.authors)
