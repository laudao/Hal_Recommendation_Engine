#-*- coding: utf-8 -*-
# filename: TopicCreation.py
# author: Laura NGUYEN
# creation date : 5/07/2017

from class_PageHal import PageHAL
from TopicGraph import TopicGraph
import os, re
from GraphObjects import *

class TopicCreation:
	def __init__(self, files, nb_passes, nb_topics, nb_words):
		self.files = files
		self.nb_passes = nb_passes
		self.nb_topics = nb_topics
		self.nb_words = nb_words

		if not(os.path.isfile("topics/topics_info.txt")):
			f = open("topics/topics_info.txt", 'w')
			f.write("nb_topics: " + str(self.nb_topics) + "\n")
			f.write("nb_words: " + str(self.nb_words) + "\n")
			for filename in self.files:
				f.write(filename + "\n")
			f.close()
			print("Created file topics_info.txt in folder topics containing num of topics per corpus, number of wordsper topic and filenames used to create the topics")
		else:
			f = open("topics/topics_info.txt", 'a')
		
			for filename in self.files:
				f.write(filename + "\n")

			f.close()	
			print("Added " + ' '.join(files) + " in topics_info.txt")

		""" indicate that topics have been added to the graph """
		f_authors = open('topics/added_topicsAuthorsGraph.txt', 'w')
		f_authors.write('1')
		f_authors.close()
		
		f_reco_authors = open('topics/added_topicsRecoAuthors.txt', 'w')
		f_reco_authors.write('1')
		f_reco_authors.close()

		f_reco_docs = open('topics/added_topicsRecoDocs.txt', 'w')
		f_reco_docs.write('1')
		f_reco_docs.close()

	@property
	def files(self):
		return self.__files

	@property
	def nb_passes(self):
		return self.__nb_passes

	@property
	def nb_topics(self):
		return self.__nb_topics

	@property
	def nb_words(self):
		return self.__nb_words

	@files.setter
	def files(self, x):
		self.__files = x
			
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
			print("nb_passes must be a positive integer")
			print("default value of nb_passes is 5")
			self.__nb_topics = 5
		
		if os.path.isfile("topics/topics_info.txt"):
			f = open('topics/topics_info.txt', 'r')
			nb_topics = int((f.readline())[11:-1])
			if nb_topics != self.nb_topics:
				print("/!\ Number of topics per corpus is different than previous value. nb_topics is assigned to previous value")
			self.__nb_topics = nb_topics
			f.close()

	@nb_words.setter
	def nb_words(self, x):
		if type(x) == int and x > 0:
			self.__nb_words = x
		else:
			print("nb_words must be a positive integer")
			print("default value of nb_words is 5")
			self.__nb_words = 5

		if os.path.isfile("topics/topics_info.txt"):
			f = open('topics/topics_info.txt', 'r')
			f.readline()
			nb_words = int((f.readline()[10:-1]))
			if nb_words != self.nb_words:
				print("/!\ Number of words per topic is different than previous value. nb_words is assigned to previous value")
			self.__nb_words = nb_words

		self.create_topic_graphs()

	def create_topic_graphs(self):
		for filename in self.files:
			page = PageHAL.create_page_file("topics/"+filename)
			t = TopicGraph(page, self.nb_passes, self.nb_topics, self.nb_words)
		print("Topics created")

	@staticmethod
	def deleteTopics():
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		
		graph.run("MATCH (n:Topic) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
		print("Topics deleted")
	
	@staticmethod
	def deleteldamodels():
		cwd = os.getcwd()
		for f in os.listdir(cwd):
			if re.search('lda.model*', f):
				os.remove(os.path.join(cwd, f))
	
		print("ldamodel files deleted")
	
	@staticmethod
	def initialize_topic_number():
		f = open('topics/topic_num.txt', 'w')
		f.write("0")
		f.close()

	@staticmethod
	def create():
		files = []
		filename = ""

		try:
			delete = int(input("Do you want to delete the previous topics? (yes:1/no:0)\n> "))
		except ValueError:
			delete = 0
		
		if delete:
			cwd = os.getcwd()
			TopicCreation.deleteTopics()
			TopicCreation.deleteldamodels()
			TopicCreation.initialize_topic_number()
			if os.path.isfile("topics/topics_info.txt"):
				os.remove(os.path.join(cwd, "topics/topics_info.txt"))
			if os.path.isfile("topics/merging_info.txt"):
				os.remove(os.path.join(cwd, "topics/merging_info.txt"))
		elif not(os.path.isfile('topics/topic_num.txt')):
			TopicCreation.initialize_topic_number()

		while filename != "-1":
			filename = input("Enter filenames from which to generate topics (-1 to stop)\n> ")
			print(filename)
			if filename == "-1":
				break

			while len(filename) == 0 or not(os.path.isfile("topics/"+filename+".txt")) or (filename+".txt") in files:
				if filename == "-1":
					break
				elif not(os.path.isfile("topics/"+filename+".txt")):
					print(filename + ".txt" + " does not exist")
				elif (filename+".txt") in files:
					print(filename+".txt" + " already selected")
				elif len(filename) == 0:
					print("Invalid input. Please try again")
				filename = input("> ")

			if filename != "-1":
				files.append(filename + ".txt")

		if files == []:
			print("No files selected")
			return
		else:
			if os.path.isfile("topics/topics_info.txt"):
				for filename in files:
					if filename in open("topics/topics_info.txt").read():
						print(filename + " has already been used to create topics")
						files.remove(filename)
			
			if files != []:
				print("You have selected the following files:")
				for filename in files:
					print("  - " + filename)
			else:
				print("No files selected")
				return 

		try:
			nb_passes = int(input("How many passes do you want the program to do? (default:50)\n> "))
		except ValueError:
			nb_passes = None

		try:
			nb_topics = int(input("How many topics per file do you want to create?\n> "))
		except ValueError:
			nb_topics = None

		try:
			nb_words = int(input("How many words do you want per topic? (default:5)\n> "))
		except ValueError:
			nb_words = None

		return TopicCreation(files, nb_passes, nb_topics, nb_words)
		
tc = TopicCreation.create()

