import py2neo
from py2neo import Graph, authenticate
import json

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

result = graph.run("MATCH (a)-[r]->(b) WITH collect({source: id(a),target: id(b),caption: type(r)}) AS edges RETURN edges")
f = open('database.json', 'w')

with open('result.json', 'w') as fp:
	for record in result:
		json.dump(record, fp, indent=2, sort_keys=True)
		fp.write('\n')

fp.close()
#	print(type(record))
#	print(type(record["edges"]))
#	for elem in record["edges"]:
#		print(elem["caption"])
#		print(elem["
#	print(type(record["edges"][0])) # dict
	
#	print(record["edges"][0].keys()) # caption: str, target: int, source: int
#	print(type(record["edges"][0]['target']))
#	f.write(record["edges"])

