import py2neo.ogm
from py2neo.ogm import *
import py2neo.database
from py2neo.database import *
from py2neo import Graph, authenticate, Node, Relationship
from GraphObjects import *

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

#graph.run("MATCH (n:Author)-[r:BELONGS_IN]->(s) DELETE r")
#graph.run("MATCH (n:Toto) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:Tata) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:Article) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:Author) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:Institution) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:Laboratory) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:Department) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
#graph.run("MATCH (n:ResearchTeam) OPTIONAL MATCH (n)-[r]-() DELETE r,n")
