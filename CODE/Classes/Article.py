# -*- coding: utf-8 -*-
# filename : Team.py
# author : Laura NGUYEN
# creation date : 20/06/2017
# contains all informations about an article

import py2neo.ogm
from py2neo.ogm import *
from Author import Author

class Article(GraphObject):
	__primarykey__ = "docid"

	docid = Property()
	title = Property()
	year = Property()
	topics = Property()
	abstract = Property()
	keywords = Property()
	article_type = Property()
	pub_date = Property()
	language = Property()

	written_by = RelatedTo(Author)

	


