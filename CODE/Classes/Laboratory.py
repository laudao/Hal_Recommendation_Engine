# -*- coding: utf-8 -*-
# filename : Laboratory.py
# author : Laura NGUYEN
# creation date : 22/06/2017
# contains all informations about a laboratory

import py2neo.ogm
from py2neo.ogm import *
from Institution import Institution

class Laboratory(GraphObject):
	__primarykey__ = "lab_id"

	lab_id = Property()
	lab_acronym = Property()
	lab_name = Property()
	lab_country = Property()

	lab_members = RelatedFrom("Author", "BELONGS_IN")
	pays = RelatedFrom("Author", "IS_PAID_BY")
	lab_children = RelatedFrom("Institution" or "Department", "IS_PART_OF")
	is_part_of = RelatedTo(Institution)

import Author
