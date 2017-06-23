# -*- coding: utf-8 -*-
# filename : URLtoDFStruct.py
# author : Laura NGUYEN
# creation date : 21/06/2017
# provides a class to extract dataframe from a json request regarding the structure
# creates structure object

import py2neo.ogm
from py2neo.ogm import *
from py2neo import Graph, authenticate
from Team import Team
import pandas as pd
import numpy as np
import urllib as ur
import requests
import json
from URLtoDF import URLtoDF

class URLtoDFStruct(URLtoDF):

	def __init__(self, url=None, df=None, struct_name=None, struct_id=None, struct_acro=None, struct_type=None, struct_parent_id=None):
		URLtoDF.__init__(self, url)
		self.struct_name = struct_name
		self.struct_id = struct_id
		self.struct_acro = struct_acro
		self.struct_type = struct_type
		self.struct_parent_id = struct_parent_id

	@property
	def struct_name(self):
		return self.__struct_name

	@property
	def struct_id(self):
		return self.__struct_id
	
	@property
	def struct_acro(self):
		return self.__struct_acro

	@property
	def struct_type(self):
		return self.__struct_type

	@property
	def struct_parent_id(self):
		return self.__struct_parent_id

	@struct_name.setter
	def struct_name(self, x):
		self.__struct_name = self.df.iloc[0]['name_s']

	@struct_id.setter
	def struct_id(self, x):
		self.__struct_id = int(self.df.reset_index().iloc[0]['docid'])
	
	@struct_acro.setter
	def struct_acro(self, x):
		self.__struct_acro = self.df.iloc[0]['acronym_s']
	
	@struct_type.setter
	def struct_type(self, x):
		self.__struct_type = self.df.iloc[0]['type_s']

	@struct_parent_id.setter
	def struct_parent_id(self, x):
		self.__struct_parent_id = self.df.iloc[0]['parentDocid_i']

	def create_struct_object(self):
			if self.struct_type == "researchteam":
				rt = ResearchTeam()
				rt.rteam_id = self.struct_id
				rt.team_acronym = self.struct_acro
				rt.rteam_name = self.struct_name
				rt.country 
				rt.parent = self.struct_parent_id
				return team
			else:
				pass

authenticate("localhost:7474", "neo4j", "stage")
url = 'https://api.archives-ouvertes.fr/ref/structure/?q=docid:408080&fl=name_s docid acronym_s type_s parentDocid_i country_s'
df = URLtoDFStruct(url)
df.printDF()
print(type(df.struct_id))
team = df.create_struct_object()
graph = Graph("http://localhost:7474/db/data/")
graph.push(team)
