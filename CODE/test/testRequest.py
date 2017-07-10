import py2neo.ogm
from py2neo.ogm import *
import py2neo.database
from py2neo.database import *
from py2neo import Graph, authenticate, Node, Relationship
from GraphObjects import *
import pandas as pd

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

req = 'MATCH (a:Author)<-[:WRITTEN_BY]-()-[:RELATED_TOPICS]->()<-[:RELATED_TOPICS]-()-[:WRITTEN_BY]->()-[:BELONGS_TO]->(struct:Laboratory) WHERE struct.struct_acronym = "LIP6" AND NOT (a)-[:BELONGS_TO]->(struct) RETURN a.auth_name'

def idIndex(a, id):
	for i in len(a):
		if a[i].id == id:
			return i
	return None

nodes = []
edges = []
