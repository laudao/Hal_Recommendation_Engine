import py2neo.ogm
from py2neo.ogm import *
import py2neo.database
from py2neo.database import *
from py2neo import Graph, authenticate, Node, Relationship
from GraphObjects import *
import pandas as pd

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

# auteurs et leurs structures qui ont ecrit un document ayant un topic en commun avec un autre article ecrit par un chercheur du LIP6 
req = 'MATCH (structAuthor)<-[:BELONGS_TO]-(a:Author)<-[:WRITTEN_BY]-()-[:RELATED_TOPICS]->()<-[:RELATED_TOPICS]-()-[:WRITTEN_BY]-()-[:BELONGS_TO]->(struct:Laboratory) WHERE struct.struct_acronym = "LIP6" AND NOT (a)-[:BELONGS_TO]->(struct) AND NOT (a)-[:BELONGS_TO]-()-[:IS_PART_OF]-(struct) AND NOT (a)-[:BELONGS_TO]-()-[:IS_PART_OF]-()-[:IS_PART_OF]->(struct) RETURN a.auth_name, structAuthor.struct_name'
print(pd.DataFrame(graph.run(req).data()))
