# -*- coding: utf-8 -*-
# filename : URLtoDF.py
# author : Laura NGUYEN
# creation date : 21/06/2017
# provides a class to extract dataframe from a json request

import pandas as pd
import numpy as np
import urllib as ur
import requests 
import json
import math

class URLtoDF:
	def __init__(self, url=None, df=None):
		self.url = url
		self.df = df

	@property
	def url(self):
		return self.__url

	@property
	def df(self):
		return self.__df

	@url.setter
	def url(self, x):
		self.__url = x
	
	@df.setter
	def df(self, x):
		self.__df = URLtoDF.generate_DF(self)

	def generate_DF(self):
		""" generates dataframe from URL """
		r = requests.get(self.url)
		dicjson = r.json()
		colonnes = ['docid', 'abstract_s', 'title_s']
		df = pd.DataFrame(dicjson['response']['docs'], columns=colonnes)
		df.set_index([df['docid']], drop=True, append=False, inplace=True, verify_integrity=False)
		df = df.drop('docid', axis=1)
		return df

	def printDF(self):
		print(self.df)

url = 'https://api.archives-ouvertes.fr/search/?q=docid:%221295622%22&fl=title_s%20abstract_s'
#url = 'https://api.archives-ouvertes.fr/ref/structure/?q=name_s:"Fairfield University"&fl=docid name_s parentDocid_i'
df = URLtoDF(url)
df.printDF()
#if math.isnan(float(df.df.iloc[0]['parentDocid_i'])):	
#	print("coucou")
