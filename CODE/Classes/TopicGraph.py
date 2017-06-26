# -*- coding: utf-8 -*-
# filename : TopicGraph.py
# author : Laura NGUYEN
# creation date : 26/06/2017

from class_ModelLDA import ModelLDA
from GraphObjects import *

class TopicGraph:
	def __init__(self, page, nb_passes, nb_topics, nb_words):
		self.page = page
		self.nb_passes = nb_passes
		self.nb_topics = nb_topics
		self.nb_words = nb_words
		self.ModelLDA = 'unknown'

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
	def modelLDA(self):
		return self.__modelLDA

	@page.setter
	def page(self, x):
		if type(x) == PageHAL:
			self.__page = x
			try:
				self.ModelLDA = "ok"
			except AttributeError:
				pass
		else:
			print("type of ", x, " must be PageHAL")
	
	@nb_passes.setter
	def nb_passes(self, x):
		if type(x) == int and x > 0:
			self.__nb_passes = x
		else:
			print("nb_passes must be a positive integer")

	@nb_topics.setter
	def nb_topics(self, x):
		if type(x) == int and x > 0:
			self.__nb_topics = x
		else:
			print("nb_topics must be a positive integer")

	@nb_words.setter
	def nb_words(self, x):
		if type(x) == int and x > 0:
			self.__nb_words = x
		else:
			print("nb_words must be a positive integer")
	
	@modelLDA.setter
	def modelLDA(self, x):
		if x == "ok":
			

