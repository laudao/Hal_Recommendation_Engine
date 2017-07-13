from class_ModelLDA import ModelLDA
from class_PageHal import PageHAL
from GraphObjects import *
import pandas as pd

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

r = graph.run('MATCH (a:Author) RETURN a').data()

for item in r:
	print(type(item['a']['auth_name']))
