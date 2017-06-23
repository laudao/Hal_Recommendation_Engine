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

class Author(GraphObject):
	__primarykey__ = "auth_id"

	auth_id = Property('auth_id')
	auth_name = Property('auth_name')
	auth_quality = Property('auth_quality')

	def __init__(self, auth_id, auth_name, auth_quality):
		self.auth_id = auth_id
		self.auth_name = auth_name
		self.auth_quality = auth_quality
	
	article = RelatedFrom("Article", "WRITTEN_BY")
	belongs_in = RelatedTo(ResearchTeam or Department or Laboratory or Institution)
	is_paid_by = RelatedTo(Laboratory or Institution)

class Article(GraphObject):
	__primarykey__ = "docid"

	docid = Property('docid')
	title = Property('title')
	year = Property('year')
	abstract = Property('abstract')
	keywords = Property('keywords')
	article_type = Property('article_type')
	pub_date = Property('pub_date')
	language = Property('language')

	def __init__(self, docid, title, year, abstract, keywords, article_type, pub_date, language):
		self.docid = docid
		self.title = title
		self.year = year
		self.abstract = abstract
		self.keywords = keywords
		self.article_type = article_type
		self.pub_date = pub_date
		self.language = language
		
	written_by = RelatedTo(Author)

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

	members = RelatedFrom("Author", "BELONGS_IN")
	
class ResearchTeam(Structure):
#	__primarykey__ = "rteam_id"
#
#	rteam_id = Property('rteam_id')
#	rteam_acronym = Property('rteam_acronym')
#	rteam_name = Property('rteam_name')
#	rteam_country = Property('rteam_country')
#
#	def __init__(self, rteam_id, rteam_acronym, rteam_name, rteam_country):
#		self.rteam_id = rteam_id
#		self.rteam_acronym = rteam_acronym
#		self.rteam_name = rteam_name
#		self.rteam_country = rteam_country

	def __init__(self, rteam_id, rteam_acronym, rteam_name, rteam_country):
		super().__init__(rteam_id, rteam_acronym, rteam_name, rteam_country)

	#members = RelatedFrom("Author", "BELONGS_IN")
	children = RelatedFrom("ResearchTeam", "IS_PART_OF")
	is_part_of = RelatedTo(Laboratory or Department or ResearchTeam or Institution)

class Department(GraphObject):
#	__primarykey__ = "dept_id"
#
#	dept_id = Property('dept_id')
#	dept_acronym = Property('dept_acronym')
#	dept_name = Property('dept_name')
#	dept_country = Property('dept_country')
#
#	def __init__(self, dept_id, dept_acronym, dept_name, dept_country):
#		self.dept_id = dept_id
#		self.dept_acronym = dept_acronym
#		self.dept_name = dept_name
#		self.dept_country = dept_country

	def __init__(self, dept_id, dept_acronym, dept_name, dept_country):
		super().__init__(dept_id, dept_acronym, dept_name, dept_country)

#	members = RelatedFrom("Author", "BELONGS_IN")
	children  = RelatedFrom("ResearchTeam" or "Department", "IS_PART_OF")
	is_part_of = RelatedTo(Department or Laboratory or Institution)

class Laboratory(GraphObject):
#	__primarykey__ = "lab_id"
#
#	lab_id = Property('lab_id')
#	lab_acronym = Property('lab_acronym')
#	lab_name = Property('lab_name')
#	lab_country = Property('lab_country')
#	
#	def __init__(self, lab_id, lab_acronym, lab_name, lab_country):
#		self.lab_id = lab_id
#		self.lab_acronym = lab_acronym
#		self.lab_name = lab_name
#		self.lab_country = lab_country

	def __init__(self, lab_id, lab_acronym, lab_name, lab_country):
		super().__init__(lab_id, lab_acronym, lab_name, lab_country)

#	members = RelatedFrom("Author", "BELONGS_IN")
	pays = RelatedFrom("Author", "IS_PAID_BY")
	children = RelatedFrom("ResearchTeam" or "Department" or "Laboratory", "IS_PART_OF")
	is_part_of = RelatedTo(Laboratory or Institution)

class Institution(GraphObject):
#	__primarykey__ = "inst_id"
#
#	inst_id = Property('inst_id')
#	inst_acronym = Property('inst_acronym')
#	inst_name = Property('inst_name')
#	inst_country = Property('inst_country')
#
#	def __init__(self, inst_id, inst_acronym, inst_name, inst_country):
#		self.inst_id = inst_id
#		self.inst_acronym = inst_acronym
#		self.inst_name = inst_name
#		self.inst_country = inst_country

	def __init__(self, inst_id, inst_acronym, inst_name, inst_country):
		super().__init__(inst_id, inst_acronym, inst_name, inst_country)

#	members = RelatedFrom("Author", "BELONGS_IN")
	pays = RelatedFrom("Author", "IS_PAID_BY")
	children = RelatedFrom("ResearchTeam" or "Department" or "Laboratory" or "Institution", "IS_PART_OF")
	is_part_of = RelatedTo(Institution)
