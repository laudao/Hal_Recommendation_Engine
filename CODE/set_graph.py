#!/usr/bin/env python

import json

from bottle import get, run, request, response, static_file
from GraphObjects import *

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")


@get("/")
def get_index():
	return static_file("index.html", root="static")


@get("/graph")
def get_graph():
	nodes = []
	rels = []
	results_inst = graph.run(
			"MATCH (i:Institution)"
			"RETURN i.struct_id as i_id, i.struct_acronym as i_acro, i.struct_name as i_name, i.struct_country as i_country"
			)
	for i_id, i_acro, i_name, i_country in results_inst:
		nodes.append({"id": i_id, "acronym": i_acro, "country": i_country, "title": i_name, "label": "institution"})

	results_lab = graph.run(
			"MATCH (l:Laboratory)"
			"RETURN l.struct_id as l_id, l.struct_acronym as l_acro, l.struct_name as l_name, l.struct_country as l_country"
			)
	for l_id, l_acro, l_name, l_country in results_lab:
		nodes.append({"id": l_id, "acronym": l_acro, "country": l_country, "title": l_name, "label": "laboratory"})

	results_dep = graph.run(
			"MATCH (d:Department)"
			"RETURN d.struct_id as d_id, d.struct_acronym as d_acro, d.struct_name as d_name, d.struct_country as d_country"
			)
	for d_id, d_acro, d_name, d_country in results_dep:
		nodes.append({"id": d_id, "acronym": d_acro, "country": d_country, "title": d_name, "label": "department"})

	results_rt = graph.run(
			"MATCH (rt:ResearchTeam)"
			"RETURN rt.struct_id as rt_id, rt.struct_acronym as rt_acro, rt.struct_name as rt_name, rt.struct_country as rt_country"
			)
	for rt_id, rt_acro, rt_name, rt_country in results_rt:
		nodes.append({"id": rt_id, "acronym": rt_acro, "country": d_country, "title": rt_name, "label": "researchteam"})
	
	results_struct = graph.run(
		"MATCH (s1)<-[r:IS_PART_OF]-(s2)"
		"RETURN s1.struct_name as s1_name, s2.struct_name as s2_name"
		)
	for s1_name, s2_name in results_struct:
		target = nodes.index(next(struct for struct in nodes if struct['title'] == s1_name))
		source = nodes.index(next(struct for struct in nodes if struct['title'] == s2_name))
		rels.append({"source": source, "target": target, "caption": "IS_PART_OF"})
	
	results = graph.run(
	    "MATCH (a:Author)<-[:WRITTEN_BY]-(d:Article)"
	    "RETURN d.title as title, collect(a.auth_name) as authors"
	    )
	i = 0
	for title, authors in results:
		nodes.append({"title": title, "label": "article"})
		source = i
		i += 1
		
		for name in authors:
			a = {"title": name, "label": "author"}
	
			try:
				target = nodes.index(a)
			except ValueError:
				nodes.append(a)
				target = i
				i+=1
			rels.append({"source": source, "target": target, "caption": "WRITTEN_BY"})
	print(rels)
	return {"nodes": nodes, "links": rels}

@get("/search")
def get_search():
	try:
		q = request.query["q"]
	except KeyError:
		return []
	else:
		results = graph.run(
	  	"MATCH (article:Article) "
	  	"WHERE article.title =~ {title} "
	  	"RETURN article", {"title": "(?i).*" + q + ".*"})
		response.content_type = "application/json"
		return json.dumps([{"article": dict(row["article"])} for row in results])


@get("/article/<title>")
def get_article(title):
	results = graph.run(
		"MATCH (article:Article {title:{title}}) "
		"OPTIONAL MATCH (a:Author)<-[r]-(article) "
		"RETURN article.title as title,"
		"collect([a.auth_name,  r.quality]) as authors "
		"LIMIT 1", {"title": title})
	row = results.next()
	return {"title": row['title'],
					"authors": [dict(zip(("name", "quality"), auth)) for auth in row['authors']]}


if __name__ == "__main__":
    run(port=8080)
