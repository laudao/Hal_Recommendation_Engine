# -*- coding: utf-8 -*-
# filename : Institution.py
# author : Laura NGUYEN
# creation date : 22/06/2017
# contains all informations about an institution

import py2neo.ogm
from py2neo.ogm import *

class Institution(GraphObject):
	__primarykey__ = "inst_id"

	inst_id = Property()
	inst_acronym = Property()
	inst_name = Property()
	inst_country = Property()

	inst_members = RelatedFrom("Author", "BELONGS_IN")
	pays = RelatedFrom("Author", "IS_PAID_BY")
	inst_children = RelatedFrom("ResearchTeam" or "Department" or "Laboratory", "IS_PART_OF")

from ResearchTeam import ResearchTeam
