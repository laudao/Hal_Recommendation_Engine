# -*- coding: utf-8 -*-
# filename : URLtoStruct.py
# author : Laura NGUYEN
# creation date : 22/06/2017
# provides a class inherited from URLtoDF to extract Author object from URL

from URLtoDF import URLtoDF
from GraphObjects import *

class URLtoAuthor(URLtoDF):
	def __init__(self, url=None, df=None):
		URLtoDF.__init__(self, url, df)

	def create_link_one_auth_node(self, auth_id, auth_name, auth_quality, auth_struct):
		a = Author(auth_id=auth_id, auth_name=auth_name, auth_quality=auth_quality)
		auth.belongs_in.add(auth_struct)
		auth_struct.members.add(auth)

	def create_link_authors(self, 

