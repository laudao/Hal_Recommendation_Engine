from GraphObjects import *

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

rt = ResearchTeam(rteam_id=100, rteam_acronym="RT", rteam_name="Research Team", rteam_country="fr")
#inst = Institution(inst_id=30, inst_acronym="INST", inst_name="INSTITUTION", inst_country="FRANCE")
#
#lab = Laboratory(lab_id = 900,lab_acronym = "LIP6",lab_name = "Laboratoire d'Informatique de Paris 6", lab_country = "France")
#lab.is_part_of.add(inst)
#
a = Author(auth_name = "Laura",auth_id = 3535002,auth_quality = "stagiaire")
#a.belongs_in.add(lab)
#a.is_paid_by.add(inst)
#
#c = Author(auth_name = "testou", auth_id = 43149293,auth_quality = "stagiaire")
#
#arti = Article(docid='78183',title='bonsoir',year=2017,abstract=None,keywords=None,article_type='revue',pub_date='12/03/2017',language='fr')
#keywords=['foo', 'bar']
#
#arti.keywords = keywords
#print(arti.keywords)
#d = Department(dept_id=98,dept_acronym='DPT',dept_name='dept',dept_country='France')

rt.members.add(a)
graph.push(rt)
print(ResearchTeam.select(graph, 100).first())
print(Structure.select(graph, 100).first())


#graph.push(arti)
#graph.push(c)
#graph.push(inst)
#graph.push(a)
#graph.push(d)
#print(Institution.select(graph, 30).first())
#print(Laboratory.select(graph, 900).first())
#print(Author.select(graph, 3535002).first())
#parent_id = 410122
#print(Institution.select(graph, parent_id).first())
#lab = Laboratory.select(graph, 900).first()
#if (lab!= None):
#	print("coucou")
#	lab.members.add(a)
	
