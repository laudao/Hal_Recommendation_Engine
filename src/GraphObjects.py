# -*- coding: utf-8 -*-
# filename : GraphObjects.py
# author : Laura NGUYEN
# creation date : 22/06/2017
# contains all objects needed for the graph

import py2neo.ogm
from py2neo.ogm import *
from py2neo import Graph, authenticate, Node, Relationship

class Author(GraphObject):
	pass
class Article(GraphObject):
	pass
class Structure(GraphObject):
	pass
class ResearchTeam(Structure):
	pass
class Department(Structure):
	pass
class Laboratory(Structure):
	pass
class Institution(Structure):
	pass
class Topic(GraphObject):
	pass

class Author(GraphObject):
	__primarykey__ = "auth_name"

	auth_name = Property('auth_name')
	
	def __init__(self, auth_name):
		self.auth_name = auth_name
	
	articles = RelatedFrom("Article", "WRITTEN_BY")
	belongs_to = RelatedTo(ResearchTeam or Department or Laboratory or Institution)
	recommended_docs = RelatedTo(Article)
	recommended_authors = Related(Author, "RELATED_AUTHORS")

class Article(GraphObject):
	__primarykey__ = "docid"

	docid = Property('docid')
	title = Property('title')
	abstract = Property('abstract')
	keywords = Property('keywords')
	article_type = Property('article_type')
	pub_date = Property('pub_date')
	language = Property('language')

	def __init__(self, docid, title, abstract, keywords, article_type, pub_date, language):
		self.docid = docid
		self.title = title
		self.abstract = abstract
		self.keywords = keywords
		self.article_type = article_type
		self.pub_date = pub_date
		self.language = language
		
	written_by = RelatedTo(Author)
	related_topics = RelatedTo(Topic)
	recommended_for = RelatedFrom("Author", "RECOMMENDED_DOCS")

class Structure(GraphObject):
	__primarykey__ = "struct_id"

	struct_id = Property("struct_id")
	struct_acronym = Property("struct_acronym")
	struct_name = Property("struct_name")
	struct_country = Property("struct_country")

	def __init__(self, struct_id, struct_acronym, struct_name, struct_country):
		self.struct_id = struct_id
		self.struct_acronym = struct_acronym
		self.struct_name = struct_name
		self.struct_country = struct_country

	members = RelatedFrom("Author", "BELONGS_TO")
	
class ResearchTeam(Structure):
	def __init__(self, rteam_id, rteam_acronym, rteam_name, rteam_country):
		super().__init__(rteam_id, rteam_acronym, rteam_name, rteam_country)

	children = RelatedFrom("ResearchTeam", "IS_PART_OF")
	is_part_of = RelatedTo(Laboratory or Department or ResearchTeam or Institution)

class Department(Structure):
	def __init__(self, dept_id, dept_acronym, dept_name, dept_country):
		super().__init__(dept_id, dept_acronym, dept_name, dept_country)

	children  = RelatedFrom("ResearchTeam" or "Department", "IS_PART_OF")
	is_part_of = RelatedTo(Department or Laboratory or Institution)

class Laboratory(Structure):
	def __init__(self, lab_id, lab_acronym, lab_name, lab_country):
		super().__init__(lab_id, lab_acronym, lab_name, lab_country)

	pays = RelatedFrom("Author", "IS_PAID_BY")
	children = RelatedFrom("ResearchTeam" or "Department" or "Laboratory", "IS_PART_OF")
	is_part_of = RelatedTo(Laboratory or Institution)

class Institution(Structure):
	def __init__(self, inst_id, inst_acronym, inst_name, inst_country):
		super().__init__(inst_id, inst_acronym, inst_name, inst_country)

	children = RelatedFrom("ResearchTeam" or "Department" or "Laboratory" or "Institution", "IS_PART_OF")
	is_part_of = RelatedTo(Institution)

class Topic(GraphObject):
	__primarykey__ = "topic_id"

	topic_id = Property("topic_id")
	sign_words = Property("sign_words")
	words_prob = Property("words_prob")

	def __init__(self, topic_id, sign_words, words_prob):
		self.topic_id = topic_id
		self.sign_words = sign_words
		self.words_prob = words_prob

	similar_topics = Related(Topic, "SIMILARITY")
	related_articles = RelatedFrom(Article, "RELATED_TOPICS")
	
