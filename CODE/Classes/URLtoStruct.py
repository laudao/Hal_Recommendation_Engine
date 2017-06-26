# -*- coding: utf-8 -*-
# filename : URLtoStruct.py
# author : Laura NGUYEN
# creation date : 22/06/2017
# provides a class inherited from URLtoDF
#  to extract ResearchTeam/Department/Laboratory/Institution object
#   from URL

from URLtoDF import URLtoDF
from GraphObjects import *

class URLtoStruct(URLtoDF):
	def __init__(self, url=None, df=None):
		URLtoDF.__init__(self, url)
		
	def create_struct_node(self):
		struct_type = self.df.iloc[0]['type_s']
		struct_id = int(self.df.reset_index().iloc[0]['docid'])
		struct_name = self.df.iloc[0]['name_s']
		struct_acro = self.df.iloc[0]['acronym_s']
		struct_parent_id = self.df.iloc[0]['parentDocid_i']
		struct_country = self.df.iloc[0]['country_s']
		struct_parent_type = self.df.iloc[0]['parentType_s']

		authenticate("localhost:7474", "neo4j", "stage")
		graph = Graph("http://localhost:7474/db/data/")
		
		if struct_type == "researchteam":
			s = ResearchTeam(rteam_id=struct_id, rteam_name=struct_name,rteam_acronym = struct_acro,rteam_country=struct_country)
		elif struct_type == "department":
			s = Department(dept_id=struct_id,dept_name=struct_name,dept_acronym=struct_acro,dept_country=struct_country)
		elif struct_type == "laboratory":
			s = Laboratory(lab_id=struct_id,lab_name=struct_name,lab_acronym=struct_acro,lab_country=struct_country)
		else:
			s = Institution(inst_id=struct_id,inst_name=struct_name,inst_acronym=struct_acro,inst_country=struct_country)
	
#		graph.push(s)

		if type(struct_parent_id) == list:
			for parent_id, parent_type in zip(struct_parent_id, struct_parent_type):
				parent = None
				if parent_type == "researchteam":
					parent = ResearchTeam.select(graph, int(parent_id)).first()
				elif parent_type == "department":
					parent = Department.select(graph, int(parent_id)).first()
				elif parent_type == "laboratory":
					parent = Laboratory.select(graph, int(parent_id)).first()
				elif parent_type == "institution":
					parent = Institution.select(graph, int(parent_id)).first()
				if parent != None:
					parent.children.add(s)
					s.is_part_of.add(parent)

		graph.push(s)

url="https://api.archives-ouvertes.fr/ref/structure/?q=docid:389588&fl=docid name_s parentDocid_i type_s acronym_s country_s parentType_s"
df = URLtoStruct(url)
df.create_struct_node()
print(type(df.df.iloc[0]['parentDocid_i']))
df.printDF()
ind = 0
print(df.df.iloc[ind]['country_s'])
