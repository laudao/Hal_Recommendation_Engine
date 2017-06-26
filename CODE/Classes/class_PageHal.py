# -*- coding: utf-8 -*-
# file name: class_PageHal
# author: Michelle MALARA
# creation date: 06\ 06\ 2017

import urllib as ur
import requests
import json
from datetime import datetime


class PageHAL:
	def __init__(self, lab=None,start_year=None, end_year=None, language='en', author=None, size=None):
		self.lab = lab
		self.start_year = start_year
		self.end_year = end_year
		self.language = language
		self.author = author
		self.size = size
		self.url = "edit"
	
	@property
	def lab(self):
		return self.__lab

	@property
	def start_year(self):
		return self.__start_year
	
	@property
	def end_year(self):
		return self.__end_year
	
	@property
	def language(self):
		return self.__language
	
	@property
	def author(self):
		return self.__author
	
	@property
	def size(self):
		return self.__size
	
	@property
	def url(self):
		return self.__url

	@lab.setter
	def lab(self, x):
		if type(x) == int:
			self.__lab = x
		elif type(x) == str and len(x) > 0:
			self.__lab = x
		else:
			self.__lab = None
		try:
			self.url = 'edit'
		except AttributeError:
			pass

	@start_year.setter
	def start_year(self, x):
		today = int(datetime.now().strftime("20%y"))
		if type(x) == int and x >= 0:
			if x<= today:
				self.__start_year = x
			else:
				self.__start_year = today
				print('start_year must be an integer between 0 and', today, ".",
				      x, '>', today, '. So end_year =', today)
		else:
			self.__start_year = None
			print('start_year must be an integer bigger than 0', x,
			      'is not. So end_year =', str(None))	
		try:
			self.url = 'edit'
		except AttributeError:
			pass
	
	@end_year.setter
	def end_year(self, x):
		today = int(datetime.now().strftime("20%y"))
		if (type(x) == int):
			if x < self.start_year:
				self.__end_year = self.start_year
				print('end_year must be an integer between', self.start_year, "and", today, '.',
			          x, '<', self.start_year, '. So end_year =', self.start_year)
			elif x > today:
				self.__end_year = today
				print('end_year must be an integer between', self.start_year, "and", today, '.',
			          x, '>', today, '. So end_year =', today)
			else:
				self.__end_year = x
		else:
			self.__end_year = today
			print('end_year must be an integer between ', self.start_year, " and ", today, '.',
		          x, 'is not. So end_year =', today)
		try:
			self.url = 'edit'
		except AttributeError:
			pass
	
	@language.setter
	def language(self, x):
		if x.upper() in "FR FRENCH FRANCAIS".split():
			self.__language = "fr"
		else:
			self.__language = "en"
			if not(x.upper() in "EN ENGLISH ANGLAIS".split()):
			    print("language must be en or fr.", x, "is not. So language is en by default")
		try:
			self.url = 'edit'
		except AttributeError:
			pass
	
	@author.setter
	def author(self, x):
		if type(x) == str and len(x) > 0:
			self.__author = x
		else:
			self.__author = None
		try:
			self.url = 'edit'
		except AttributeError:
			pass
	
	@size.setter
	def size(self, x):
		if type(x) != int:
			self.__size = 30
			print("size must be an integer between 0 and 10000.", x, "is not. So size = 30 by default")
		else:
			if x < 0:
			    self.__size = 0
			    print("The minimum size is 0.", x, "< 0. So size = 0")
			elif x > 10000:
			    self.__size = 10000
			    print("The bigger size is 10000", x, "> 10000. So size = 10000")
			else:
			    self.__size = x
		try:
			self.url = 'edit'
		except AttributeError:
			pass
	
	@url.setter
	def url(self, x):
		self.__url = PageHAL.generate_url(self.lab,self.start_year, self.end_year,
		                                  self.language, self.author, self.size)
		if x != "edit":
			print("you cant modify the url")
	
	@staticmethod
	def generate_url(lab,pstart, pend, language, author, size):
		"""create url for the search in HAL.
		Return title, keys words and abstract in language"""
		url = 'https://api.archives-ouvertes.fr/search/?fl=title_s,' + language + '_keyword_s,abstract_s'
		if type(lab) == str:
			url += '&fq=labStructAcronym_s:' + lab.upper()  # restrict labo name
		elif type(lab) == int:
			url += '&fq=labStructId_i:' + str(lab)  # restrict id labo
		if not(pstart is None):  # restrict period
			url += '&fq=producedDateY_i:[' + str(pstart) + ' TO ' + str(pend) + ']'
		else:
			url += '&fq=producedDateY_i:[* TO ' + str(pend) + ']'
		if not(author is None):
			url += '&fq=authFullName_s:"' + author + '"'
		url += '&fq=language_s:' + language
		if not(size is None):
			url += '&rows=' + str(size)  # nb result
		return url
		
	def collect(self):
		"""collect information on the HAL page (title, keys words and abstract)"""
		page = ur.urlopen(self.url)
		data = page.read()
		encoding = page.info().get_content_charset('utf-8')
		return data.decode(encoding)
	
	def collect_in_file(self, filename):
		"""Saves HAL page information in a file named filename"""
		file = open(filename, 'w')
		res = self.collect()
		file.write(res)
		file.close()
	
	def extract(self):
		"""return a list of Tuple (id_doc, text_doc) for doc in HAL page which have a text"""
		r = requests.get(self.url)
		dicjson = r.json()
		res = []
		doc = 0
		for dic in dicjson['response']['docs']:
			title = dic['title_s'][0]
			text = ''
			keyword = self.language + '_keyword_s'
			if keyword in dic:
				for word in dic[keyword]:
					text += word + ' '
			if 'abstract_s' in dic:
				abstract = dic['abstract_s'][0]
				if not(abstract in ['no abstract', 'absent']):
					text += abstract
			if text:
				res.append((doc, title + text))
				doc += 1
		return res
	
	def extract_title(self):
		"""return a list of Tuple (id_doc, text_doc) for doc in HAL page which have a text or just title"""
		r = requests.get(self.url)
		dicjson = r.json()
		res = []
		doc = 0
		for dic in dicjson['response']['docs']:
			text = dic['title_s'][0]
			keyword = self.language + '_keyword_s'
			if keyword in dic:
				for word in dic[keyword]:
					text += word + ' '
			if 'abstract_s' in dic:
				abstract = dic['abstract_s'][0]
				if not (abstract in ['no abstract', 'absent']):
					text += abstract
			if text:
				res.append((doc, text))
				doc += 1
		return res
	
	def generate_file_name(self):
		"""return 'self.lab'-from_'self.start_year'_to_'self.end_year'-'self.language'-size_'self.size'.txt"""
		filename = ''
		if not(self.lab is None):
			filename += str(self.lab.upper) + '-'
		if not(self.start_year is None):
			filename += 'from_' + str(self.start_year) + '_to_' + str(self.end_year) + "-"
		filename += self.language
		if not(self.author is None):
			filename += '-by_' + self.author
		if not(self.size is None):
			filename += '-size_' + str(self.size)
		filename += '.txt'
		return filename
	
	def extract_in_file(self, filename=None):
		"""return a file containing a list of Tuple (id_doc, text_doc) for doc in HAL page which have a text.
		the file is named filename or, if there are not, self.generate-file-name()"""
		corpus = self.extract()
		if filename is None:
			filename = self.generate_file_name()
		file = open(filename, 'w')
		writing = ''
		if not(self.lab is None):
			writing += 'Structure: ' + str(self.lab) + '\n\n'
		if self.start_year is None:
			writing += 'from *'
		else:
			writing += 'from ' + str(self.start_year)
		writing += ' to ' + str(self.end_year) + '\n\nLanguage: ' + self.language + '\n\n'
		if not(self.author is None):
			writing += 'Author: ' + self.author + '\n\n'
		writing += 'Size corpus: ' + str(len(corpus)) + '\n\nurl:\n' + self.url + '\n\n'
		file.write(writing)
		json.dump(corpus, file)
		file.close()
	
	@staticmethod
	def create_page_questions():
		"""collect information for create HAL page by asking questions"""
		start_date = input('start year (integer ----)(none if not):')
		try:
			start_date = int(start_date)
		except ValueError:
			start_date = None
		end_date = input('end year (integer ----)(none if not):')
		try:
			end_date = int(end_date)
		except ValueError:
			end_date = None
		lab = input('acronym structure (ex: lip6)(none if not):')
		if lab == 'none':
			lab = input('id structure (integer)(none if not):')
			try:
				lab = int(lab)
			except ValueError:
				lab = None
		author = input('Full name of the author (none if not):')
		if author == 'none':
			author = None
		language = input('diminutive language (default : "en"):')
		size = input('number of result (default : 30):')
		try:
			size = int(size)
		except ValueError:
			pass
		return PageHAL(lab, start_date, end_date, language, author, size)
	
	@staticmethod
	def create_page_file(file_name):
		"""collect information for create HAL page in file named file_name"""
		f = open(file_name, 'r')
		l = f.readline()
		lab = l[11:-1]
		try:
			lab = int(lab)
		except ValueError:
			pass
		l = f.readline()
		start_date = l[5:-1]
		try:
			start_date = int(start_date)
		except ValueError:
			start_date = None
		l = f.readline()
		end_date = l[3:-1]
		try:
			end_date = int(end_date)
		except ValueError:
			end_date = None
		l = f.readline()
		language = l[10:-1]
		l = f.readline()
		author = l[8:-1]
		l = f.readline()
		size = l[18:-1]
		try:
			size = int(size)
		except ValueError:
			size = None
		f.close()
		return PageHAL(lab, start_date, end_date, language, author, size)
