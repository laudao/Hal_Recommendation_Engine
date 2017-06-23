# -*- coding: utf-8 -*-
# filename : Department.py
# author : Laura NGUYEN
# creation date : 22/06/2017
# contains all informations about a department

import py2neo.ogm
from py2neo.ogm import *
from Institution import Institution
from Laboratory import Laboratory


class Department(GraphObject):
	__primarykey__ = "dept_id"

	dept_id = Property()
	dept_acronym = Property()
	dept_name = Property()
	dept_country = Property()

	dept_members = RelatedFrom("Author", "BELONGS_IN")
	dept_children  = RelatedFrom("ResearchTeam", "IS_PART_OF")
	is_part_of = RelatedTo(Laboratory or Institution)


