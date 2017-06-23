# -*- coding: utf-8 -*-
# filename : Team.py
# author : Laura NGUYEN
# creation date : 20/06/2017
# contains all informations about an author

import py2neo.ogm
from py2neo.ogm import *
from ResearchTeam import ResearchTeam
from Department import Department
from Laboratory import Laboratory
from Institution import Institution

class Author(GraphObject):
	__primarykey__ = "auth_id"

	auth_id = Property()
	auth_name = Property()
	auth_quality = Property()

	article = RelatedFrom("Article", "WRITTEN_BY")
	belongs_in = RelatedTo(ResearchTeam or Department or Laboratory or Institution)
	is_paid_by = RelatedTo(Laboratory or Institution)

import Article
