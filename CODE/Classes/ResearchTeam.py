# -*- coding: utf-8 -*-
# filename : ResearchTeam.py
# author : Laura NGUYEN
# creation date : 20/06/2017
# contains all informations about research team
import py2neo.ogm
from py2neo.ogm import *
from Laboratory import Laboratory
from Department import Department
from Institution import Institution

class ResearchTeam(GraphObject):
	__primarykey__ = "rteam_id"

	rteam_id = Property()
	rteam_acronym = Property()
	rteam_name = Property()
	rteam_country = Property()

	rteam_members = RelatedFrom("Author", "BELONGS_IN")
	is_part_of = RelatedTo(Laboratory or Department or Institution)


