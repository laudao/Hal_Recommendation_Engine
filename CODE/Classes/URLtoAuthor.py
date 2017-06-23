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

	def create_one_auth_node(self, a_id, a_name, a_quality, a_struct):
		a = Author(auth_id=a_id, auth_name=a_name, auth_quality=a_quality)
		a.belongs_in.add(a_struct)


