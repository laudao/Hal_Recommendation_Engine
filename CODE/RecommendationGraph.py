# -*- coding: utf-8 -*-
# filename : RecommendationGraph.py
# author : Laura NGUYEN
# creation date : 3/07/2017

from GraphObjects import *
import pandas as pd

class RecommendationGraph:
	def __init__(self, recommendation):
		self.recommendation = recommendation
#		self.auth_name = auth_name

	@property
	def recommendation(self):
		return self.__recommendation

#	@property
#	def auth_name(self):
#		return self.__auth_name

	@recommendation.setter
	def recommendation(self, x):
		self.__recommendation = x
		if self.recommendation == 1:
			print("Get top recommended articles")
			self.getTopArticles()
		elif self.recommendation == 2:
			print("Get top recommended authors")
			self.getTopAuthors()

#	@auth_name.setter
#	def auth_name(self, x):
#		self.__auth_name = x
#		print(self.auth_name)
#		if self.recommendation == 1:
#			print("Get top recommended articles")
#			self.getTopArticles()
#		elif self.recommendation == 2:
#			print("Get top recommended authors")
#			self.getTopAuthors()
	
	def link_recommended_authors(self, graph, a1):
		""" get authors who have written articles whose topics are similar to those of articles written by a1 """
		r = graph.run('MATCH (s1)<-[:BELONGS_TO]-(a1:Author)<-[:WRITTEN_BY]-()-[r1:RELATED_TOPICS]->()<-[r2:RELATED_TOPICS]-()-[:WRITTEN_BY]->(a2:Author)-[:BELONGS_TO]->(s2) WHERE a1.auth_name = "' + a1.auth_name + '" AND NOT a1 = a2 AND NOT ((a1)-[:BELONGS_TO]->()<-[:BELONGS_TO]-(a2)) RETURN a2.auth_name, r1.weight, r2.weight')
		df = pd.DataFrame(r.data())

		if not(df.empty):
			df = df.set_index(df["a2.auth_name"])
			df = df.drop("a2.auth_name", axis=1)
			df["weight"] = df["r1.weight"]*df["r2.weight"]
			df = df.drop("r1.weight", axis=1)
			df = df.drop("r2.weight", axis=1)
			df = df.sort_values("weight", axis=0, ascending=False).head(5)
	
			authors = []
		
			for row in df.itertuples():
				""" link authors """
				a2 = Author.select(graph).where('_.auth_name = "' + row[0] + '"').first()
	
				graph.run('MATCH (a1:Author), (a2:Author) WHERE a1.auth_name = "' + a1.auth_name + '" AND a2.auth_name = "' + a2.auth_name + '" CREATE (a1)-[r:RECOMMENDED_AUTHORS {weight: ' + str(row[1]) + '}]->(a2)')
		#		print("Linking " + a1.auth_name + " and " + a2.auth_name)
				graph.push(a2)
		#		graph.push(a1)
	
				if a2.auth_name not in authors:
					authors.append(a2.auth_name)
	
			graph.push(a1)
			print(authors)
		else:
			print("Can't get any recommended author for " + a1.auth_name)

	def link_recommended_docs(self, graph, a):
		""" get documents whose topics are similar to those of articles written by a """
		r = graph.run('MATCH (a:Author)<-[:WRITTEN_BY]-()-[r1:RELATED_TOPICS]->()<-[r2:RELATED_TOPICS]-(doc:Article) WHERE a.auth_name = "' + a.auth_name +'" AND NOT (doc)-[:WRITTEN_BY]->(a) RETURN doc.docid, doc.title, r1.weight, r2.weight')
		
		df = pd.DataFrame(r.data())
	
		if not df.empty:
			df = df.set_index(df["doc.docid"])
			df = df.drop("doc.docid", axis=1)
			df["weight"] = df["r1.weight"] * df["r2.weight"]
			df = df.sort_values("weight", axis=0, ascending=False).head(10)
			docs = []

			for row in df.itertuples():
				""" link article and author """
				doc = Article.select(graph, int(row[0])).first()

				graph.run('MATCH (a:Author), (d:Article) WHERE a.auth_name = "' + a.auth_name + '" AND d.docid = '+ str(doc.docid) + ' CREATE (a)-[r:RECOMMENDED_DOCS {weight: ' + str(row[4]) + '}]->(d)')
		#		print("Linking " + a.auth_name + " and article " + doc.title)
#				graph.push(a)
				graph.push(doc)

				if row[1] not in docs:
					docs.append(row[1])

			graph.push(a)
			print(docs)
		else:
			print("Can't get related articles for " + a.auth_name)

	def getTopAuthors(self):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		
		f = open('topics/added_topicsRecoAuthors.txt', 'r')
		added_topics = int(f.readline())
		f.close()

#		a1 = Author.select(graph).where('_.auth_name = "' + self.auth_name + '"').first()
		r = graph.run('MATCH (a:Author) RETURN a').data()

		for author in r:
			name = author['a']['auth_name']
			a1 = Author.select(graph, name).first()
	
			link_exists = ((graph.run('MATCH (a:Author)-[r:RECOMMENDED_AUTHORS]->() WHERE a.auth_name = "' + a1.auth_name + '" RETURN COUNT(r)')).data())[0]['COUNT(r)']
			
			""" if topics have been added """
			if added_topics:
				""" author is already linked to other authors, delete relationships """
				if link_exists > 0:
					print("Deleted recommendations for " + a1.auth_name)
					graph.run('MATCH (a:Author)-[r:RECOMMENDED_DOCS]->(d:Article) WHERE a.auth_name = "' + a1.auth_name + '" DELETE r')
#					graph.push(a1)
				
				""" create new recommendations"""
				self.link_recommended_authors(graph, a1)
					
			else:
				""" no topic has been added but author doesn't have any recommendation """
				if link_exists == 0:						
					self.link_recommended_authors(graph, a1)
				else:
					print(a1.auth_name + " already has recommendations")
		
		f = open('topics/added_topicsRecoAuthors.txt', 'w')
		f.write('0')
		f.close()
	
	def getTopArticles(self):
		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")

		f = open('topics/added_topicsRecoDocs.txt', 'r')
		added_topics = int(f.readline())
		f.close()
	
		r = graph.run('MATCH (a:Author) RETURN a').data()

		""" get recommended articles for every author """
		for author in r:
			name = author['a']['auth_name']
			a = Author.select(graph, name).first()

			link_exists = ((graph.run('MATCH (a:Author)-[r:RECOMMENDED_DOCS]->() WHERE a.auth_name = "' + a.auth_name + '" RETURN COUNT(r)')).data())[0]['COUNT(r)']

			""" if topics have been added, change recommendations """
			if added_topics:
				""" author already has recommendations, delete relationships """
				if link_exists > 0:
					print("Deleted recommendations for " + a.auth_name)
					graph.run('MATCH (a:Author)-[r:RECOMMENDED_DOCS]->(d:Article) WHERE a.auth_name = "' + a.auth_name + '" DELETE r')
#					graph.push(a)

				""" create new recommendations """
				self.link_recommended_docs(graph, a)

			else:
				""" no topic has been added but author doesn't have any recommendation """
				if link_exists == 0:
					self.link_recommended_docs(graph, a)
				else:
					print(a.auth_name + " already has recommendations")
		
		f = open('topics/added_topicsRecoDocs.txt', 'w')
		f.write('0')
		f.close()

	@staticmethod
	def create_recommendation():
		print(" 1 - Get top 10 recommended articles for each author")
		print(" 2 - Get top 5 recommended authors for each author")

		print("Please select among the choices above (enter the number)")
		try:
			choice = int(input("> "))
		except ValueError:
			choice = None

		while choice not in range(1, 3):
			choice = int(input("Invalid input. Please retry\n> "))
				
#		print("Enter the author's name")
#
#		try:
#			name = input("> ")
#		except ValueError:
#			name = None
#
#		while not(name) or type(name) != str:
#			name = input("Invalid input. Please retry\n> ")
				
		if choice == 1:
			return RecommendationGraph(1)
		elif choice == 2:
			return RecommendationGraph(2)
			
rg = RecommendationGraph.create_recommendation()		
