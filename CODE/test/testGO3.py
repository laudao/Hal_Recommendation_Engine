import py2neo.ogm
from py2neo.ogm import *
import py2neo.database
from py2neo.database import *
from py2neo import Graph, authenticate, Node, Relationship
from GraphObjects import *
import pandas as pd

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

#class Toto(GraphObject):
#	__primarykey__ = "toto_id"
#
#	toto_id = Property('toto_id')
#
#	def __init__(self, toto_id):
#		self.toto_id = toto_id
#
#	tata = RelatedFrom("Tata", "TOTO_IS")
#
#class Tata(GraphObject):
#	__primarykey__ = "tata_id"
#
#	tata_id = Property('tata_id')
#
#	def __init__(self, tata_id):
#		self.tata_id = tata_id
#
#	toto_is = RelatedTo(Toto)
#
#t = Toto(-409)
#ta = Tata(-12)
#ta.toto_is.add(t)
#graph.push(t)
#graph.push(ta)
#struct = "CNRS"
#query1 = 'MATCH(l:Laboratory) WHERE l.struct_acronym = "LIP6" RETURN l.struct_name, l.struct_acronym, l.struct_id'
#query = 'MATCH(a:Author)-[:BELONGS_IN]-()-[:IS_PART_OF]-()-[:IS_PART_OF]-()-[:IS_PART_OF]->(:Institution{struct_name:' + '"' + struct + '"' + '}) RETURN a.auth_name LIMIT 0'
#print(pd.DataFrame(graph.run(query).data()))

q = graph.run("MATCH (a:Author) RETURN a")
#print(pd.DataFrame(q.data()))
#qq = ((graph.run("MATCH (a:Author)-[r:BELONGS_TO]-(rt:Laboratory) WHERE a.auth_name='Thierry Monteil' RETURN COUNT(r)")).data())[0]['COUNT(r)']
#print(qq)
#res = qq.data()
#print(res[0]['COUNT(r)'])
#qqq = graph.run("MATCH (a:Article) RETURN a.docid")
#col = ['a.docid', 'a.title', 'a.abstract', 'a.keywords', 'a.article_type', 'a.pub_date', 'a.language']
#df = pd.DataFrame(qqq.data())
#print(df.head())

#row = df.iloc[0]
#print(type(row['a.docid']))
#print(type(row['a.title']))
#print(type(row['a.abstract']))
#print(type(row['a.keywords']))
#print(type(row['a.article_type']))
#print(type(row['a.pub_date']))
#print(type(row['a.language']))

#qqqq = graph.run("MATCH (t1:Topic)-[r:SIMILARITY]-(t2:Topic) WHERE t1.topic_id = 5 AND t2.topic_id = 8 RETURN r.kwproperties")
#print(pd.DataFrame(qqqq.data()))

#auth = "Delphine Luquet"
#r = graph.run('MATCH (a:Author) WHERE a.auth_name = "' + auth + '" RETURN a')
#auth = Author.select(graph).where("_.auth_name = 'Delphine Luquet'").first()
#print(auth.auth_name)

#r = graph.run("MATCH (a:Author)<-[:WRITTEN_BY]-()-[r1:RELATED_TOPICS]->()<-[r2:RELATED_TOPICS]-(doc:Article) WHERE a.auth_name = 'Eric Bourreau' AND NOT (doc)-[:WRITTEN_BY]->(a) RETURN doc.docid, doc.title, r1.weight, r2.weight")
#r = graph.run("MATCH (s1)<-[:BELONGS_TO]-(a1:Author)<-[:WRITTEN_BY]-()-[r1:RELATED_TOPICS]->()<-[r2:RELATED_TOPICS]-(doc:Article)-[r3:WRITTEN_BY]->(a2:Author)-[:BELONGS_TO]->(s2) WHERE a1.auth_name = 'Eric Bourreau' AND NOT a1 = a2 AND NOT ((a1)-[:BELONGS_TO]->()<-[:BELONGS_TO]-(a2)) RETURN a2.auth_name, s2.struct_name, r1.weight, r2.weight")
#df = pd.DataFrame(r.data())
#df = df.set_index(df["a2.auth_name"])
#df = df.drop("a2.auth_name", axis=1)
#df["weight"] = df["r1.weight"]*df["r2.weight"]
#df = df.sort_values("weight", axis=0, ascending=False)
#df = df.drop("r1.weight", axis=1)
#df = df.drop("r2.weight", axis=1)
#df = df.drop("doc.docid", axis=1)
#df["weight"] = df["r1.weight"]*df["r2.weight"]
#df = df.sort_values("weight", axis=0, ascending=False).head(10)
#print(df)
#print(df)

#for row in df.itertuples():
#	print(row[0])

#r = graph.run("MATCH (rt:ResearchTeam) WHERE NOT((rt)-[:IS_PART_OF]->()) RETURN rt.struct_name")
#r = graph.run("MATCH (a:Author) WHERE NOT((a)-[:BELONGS_TO]->()) RETURN a.auth_name, a.auth_quality")
#df = pd.DataFrame(r.data())
#print(df)

#n = graph.run("MATCH (t:Topic) RETURN MAX(t.topic_id)")
#df = pd.DataFrame(n.data())
#print(df.iloc[0]['MAX(t.topic_id)'])
#print((pd.DataFrame((graph.run("MATCH (t:Topic) RETURN MAX(t.topic_id)")).data())).iloc[0]['MAX(t.topic_id)'])

#keywords = ['Linear optimisation','Bi','Assignment problem','Label - wise decomposition','Label ranking','Imprecise probability','Partial predictions']
##keywords = "'Linear optimisation','Bi','Assignment problem','Label - wise decomposition','Label ranking','Imprecise probability','Partial predictions'"
#print("','".join(keywords))
#a = Article.select(graph, 1166139).first()
#print(type(a.keywords))
#print(a.keywords)
#b = Article.select(graph).where("_.keywords = ['" + "','".join(keywords) + "']").first()
#print(b.docid)
#print(b.keywords)

#id_min = (pd.DataFrame((graph.run("MATCH (t:Topic) RETURN MAX(t.topic_id)")).data())).iloc[0]['MAX(t.topic_id)']
#print(id_min)
