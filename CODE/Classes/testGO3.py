import py2neo.ogm
from py2neo.ogm import *
import py2neo.database
from py2neo.database import *
from py2neo import Graph, authenticate, Node, Relationship
from GraphObjects import *
import pandas as pd

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

class Toto(GraphObject):
	__primarykey__ = "toto_id"

	toto_id = Property('toto_id')

	def __init__(self, toto_id):
		self.toto_id = toto_id

	tata = RelatedFrom("Tata", "TOTO_IS")

class Tata(GraphObject):
	__primarykey__ = "tata_id"

	tata_id = Property('tata_id')

	def __init__(self, tata_id):
		self.tata_id = tata_id

	toto_is = RelatedTo(Toto)

t = Toto(-409)
ta = Tata(-12)
ta.toto_is.add(t)
graph.push(t)
graph.push(ta)
#struct = "CNRS"
#query1 = 'MATCH(l:Laboratory) WHERE l.struct_acronym = "LIP6" RETURN l.struct_name, l.struct_acronym, l.struct_id'
#query = 'MATCH(a:Author)-[:BELONGS_IN]-()-[:IS_PART_OF]-()-[:IS_PART_OF]-()-[:IS_PART_OF]->(:Institution{struct_name:' + '"' + struct + '"' + '}) RETURN a.auth_name LIMIT 0'
#print(pd.DataFrame(graph.run(query).data()))




