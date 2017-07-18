#!/usr/bin/env python
# -*- coding: utf-8 -*-
# taken from Neo4j examples: https://github.com/neo4j-examples/movies-python-py2neo-3.0
# modified by Laura Nguyen
# creation date : 7/07/2017

import json

from bottle import get, run, request, response, static_file
from GraphObjects import *

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")


@get("/")
def get_index():
	return static_file("index.html", root="static")


@get("/searchArticle")
def get_search_article():
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

@get("/searchAuthor")
def get_search_author():
	try:
		q = request.query["q"]
	except KeyError:
		return []
	else:
		results = graph.run(
	  	"MATCH (author:Author) "
	  	"WHERE author.auth_name =~ {name} "
	  	"RETURN author", {"name": "(?i).*" + q + ".*"})
		response.content_type = "application/json"
		return json.dumps([{"author": dict(row["author"])} for row in results])

@get("/searchStructure")
def get_search_structure():
	try:
		q = request.query["q"]
	except KeyError:
		return []
	else:
		results = graph.run(
	  	"MATCH (structure) "
	  	"WHERE structure.struct_name =~ {name} "
	  	"RETURN structure", {"name": "(?i).*" + q + ".*"})
		response.content_type = "application/json"
		return json.dumps([{"structure": dict(row["structure"])} for row in results])

@get("/article/<title>")
def get_article(title):
	results = graph.run(
		"MATCH (article:Article {title:{title}}) "
		"OPTIONAL MATCH (a:Author)<-[r]-(article) "
		"RETURN article.title as title, "
		"article.docid as docid, " 
		"article.abstract as abstract, "
		"article.keywords as keywords, " 
		"article.article_type as article_type, " 
		"article.pub_date as pub_date, " 
		"article.language as language, "
		"collect([a.auth_name,  r.quality]) as authors "
		"LIMIT 1", {"title": title}
		)
	row = results.next() 

	results_topics = graph.run(
		'MATCH (d:Article {title: {title}}) '
		'OPTIONAL MATCH (t)<-[:RELATED_TOPICS]-(d) '
		'RETURN collect(distinct [t.sign_words]) as topics '
		'LIMIT 1', {"title":title}
		)
	row_topics = results_topics.next()

	return {"title": row['title'], 
					"docid": row['docid'],
					"abstract": row['abstract'],
					"keywords": row['keywords'],
					"type": row['article_type'],
					"pub_date": row['pub_date'],
					"language": row['language'],
					"topics": [dict(zip(("words",), topic)) for topic in row_topics['topics']],
					"authors": [dict(zip(("name", "quality"), auth)) for auth in row['authors']]}

@get("/article_graph/<title>")
def get_article_graph(title):
	results = graph.run(
		"MATCH (article:Article {title:{title}}) "
		"OPTIONAL MATCH (s)<-[:BELONGS_TO]-(a:Author)<-[r]-(article) "
		"RETURN article.title as title,"
		"collect([a.auth_name,  r.quality, s.struct_acronym, s.struct_name, labels(s)[0]]) as authors "
		"LIMIT 1", {"title": title})
	
	nodes = []
	rels = []
	i=0
	for title, authors in results:
		nodes.append({"title": title, "label": "article"})
		source = i
		i+=1
		for name, quality, acronym, s_name, label in authors:
			author = {"title": name, "quality": quality, "label": "author"}
			try:
				target = nodes.index(author)
			except ValueError:
				nodes.append(author)
				target = i
				i+=1
			struct = {"title": s_name, "acronym": acronym, "label": label.lower()}
			try:
				target_struct = nodes.index(struct)
			except ValueError:
				nodes.append(struct)
				target_struct = i
				i+=1

			rels.append({"source": source, "target": target, "caption": "WRITTEN_BY"})
			rels.append({"source": target, "target": target_struct, "caption": "BELONGS_TO"})
	print(nodes)
	print(rels)
	return {"nodes": nodes, "links": rels}

@get("/author/<name>")
def get_author(name):
	results_struct = graph.run(
		"MATCH (a:Author {auth_name:{name}}) "
		"OPTIONAL MATCH (a:Author)-[r:BELONGS_TO]->(s) "
		"RETURN a.auth_name as name, "
		"collect([s.struct_name]) as structures "
		"LIMIT 1", {"name": name}
		)

	row_struct = results_struct.next()

	results_docs = graph.run(
		"MATCH (a:Author {auth_name:{name}}) "
		"OPTIONAL MATCH (d:Article)-[:WRITTEN_BY]->(a) "
		"RETURN collect([d.title]) as articles "
		"LIMIT 1", {"name": name}
		)
	row_docs = results_docs.next()

	results_topics = graph.run(
		"MATCH (a:Author {auth_name:{name}}) "
		"OPTIONAL MATCH (t)<-[:RELATED_TOPICS]-()-[:WRITTEN_BY]->(a) "
		"RETURN collect([t.topic_id, t.sign_words]) as topics "
		"LIMIT 1", {"name": name}
		)

	row_topics = results_topics.next()
	print(row_docs)

	results_docs_recommendations = graph.run(
		"MATCH (a: Author {auth_name:{name}}) "
		"OPTIONAL MATCH (d)<-[r:RECOMMENDED_DOCS]-(a) "
		"RETURN collect([d.title, r.weight]) as recommended_docs "
		"LIMIT 1", {"name": name}
		)
	results_authors_recommendations = graph.run(
		"MATCH (a1: Author {auth_name:{name}}) "
		"OPTIONAL MATCH (a2)<-[r:RECOMMENDED_AUTHORS]-(a1) "
		"RETURN collect([a2.auth_name, r.weight]) as recommended_authors " 
		"LIMIT 1", {"name": name}
		) 
	row_reco_docs = results_docs_recommendations.next()
	row_reco_authors = results_authors_recommendations.next()
	print(row_reco_docs['recommended_docs'])
	return {"name": row_struct['name'], 
					"articles": [dict(zip(("title",), article)) for article in row_docs['articles']],
					"topics": [dict(zip(("id", "words"), topic)) for topic in row_topics['topics']],
					"structures": [dict(zip(("struct_name",), structure)) for structure in row_struct['structures']],
					"recommended_docs": [dict(zip(("title", "weight"), recommended_doc)) for recommended_doc in row_reco_docs['recommended_docs']],
					"recommended_authors": [dict(zip(("name", "weight"), recommended_author)) for recommended_author in row_reco_authors['recommended_authors']]}

@get("/recommended_authors/<name>")
def get_recommended_authors(name):
	results = graph.run(
		"MATCH (a1:Author {auth_name: {name}}) "
		"OPTIONAL MATCH (a2:Author)<-[r:RECOMMENDED_AUTHORS]-(a1) "
		"RETURN collect([a2.auth_name, r.weight]) as recommended_authors "
		"LIMIT 1", {"name": name})
	row = results.next()
	return {"recommended_authors": [dict(zip(("name", "weight"), auth)) for auth in row['recommended_authors']]} 

@get("/recommended_docs/<name>")
def get_recommended_docs(name):
	results = graph.run(
		"MATCH (a:Author {auth_name: {name}}) "
		"OPTIONAL MATCH (a)-[r:RECOMMENDED_DOCS]->(d:Article) "
		"RETURN collect([d.title, r.weight]) as recommended_docs "
		"LIMIT 1", {"name": name})
	row = results.next()
	return {"recommended_docs": [dict(zip(("title", "weight"), doc)) for doc in row['recommended_docs']]}

@get("/topics_graph")
def get_topics():
	nodes = []
	rels = []
	results = graph.run(
		"MATCH (t:Topic) "
		"RETURN t.topic_id as topic_id, t.sign_words as words, t.words_prob as weights"
		)
	for topic_id, words, weights in results:
		nodes.append({"id": topic_id, "words": words, "weights": weights, "label": "topic"})

	results = graph.run(
		"MATCH (t1)-[r:SIMILARITY]-(t2) "
		"RETURN t1.topic_id as t1_id, t1.sign_words as words1, t1.words_prob as weights1, "
		"t2.topic_id as t2_id, t2.sign_words as words2, t2.words_prob as weights2, r.kwproperties as sim"
		)
	i=0
	for t1_id, words1, weights1, t2_id, words2, weights2, sim in results:
		topic1 = {"id": t1_id, "words": words1, "weights": weights1, "label": "topic"}
		topic2 = {"id": t2_id, "words": words2, "weights": weights2, "label": "topic"}
		source = nodes.index(topic1)
		target = nodes.index(topic2)

		rels.append({"source": source, "target": target, "caption": "SIMILARITY"})
	return {"nodes": nodes, "links": rels}

@get("/structure/<name>")
def get_structure(name):
	print(name)
	results_children = graph.run(
		'MATCH (s {struct_name:{name}}) '
		'OPTIONAL MATCH (c)-[:IS_PART_OF]->(s) '
		'RETURN s.struct_name as name, '
		's.struct_id as id, '
		's.struct_acronym as acronym, '
		's.struct_country as country, '
		'labels(s) as type, '
		'collect([c.struct_name, c.struct_acronym, labels(c)[0]]) as children '
		'LIMIT 1', {"name": name}
		)
	results_parents = graph.run(
		'MATCH (s {struct_name:{name}}) '
		'OPTIONAL MATCH (s)-[:IS_PART_OF]->(p) '
		'RETURN collect([p.struct_name, p.struct_acronym, labels(p)[0]]) as parents '
		'LIMIT 1', {"name": name}
		)

	results_topics = graph.run(
		'MATCH (s {struct_name: {name}}) '
		'OPTIONAL MATCH (t)<-[:RELATED_TOPICS]-()-[:WRITTEN_BY]->(a:Author)-[:BELONGS_TO]->(s) '
		'RETURN collect(distinct [t.sign_words]) as topics '
		'LIMIT 1', {"name":name}
		)
	print(results_children.data())
	print(results_parents.data())
	row_children = results_children.current() 
	row_parents = results_parents.current()
	row_topics = results_topics.next()
	print(row_children)
	print(row_parents)
	print(row_topics)

	return {"name": row_children['name'], 
					"id": row_children['id'],
					"acronym": row_children['acronym'],
					"country": row_children['country'],
					"type": row_children['type'],
					"children": [dict(zip(("name", "acronym", "type"), child)) for child in row_children['children']],
					"parents": [dict(zip(("name", "acronym", "type"), parent)) for parent in row_parents['parents']],
					"topics": [dict(zip(("words",), topic)) for topic in row_topics['topics']]}

@get("/structure_graph/<name>")
def get_structure_graph(name):
	nodes = []
	rels = []
	i=0

	results_children = graph.run(
		"MATCH (s {struct_name: {name}}) "
		"OPTIONAL MATCH (c)-[r:IS_PART_OF]->(s) "
		"RETURN s.struct_name as name, s.struct_acronym as acronym, labels(s)[0] as type, "
		"collect([c.struct_name, labels(c)[0]]) as children "
		"LIMIT 1", {"name": name}
		)
	for name, acronym, type, children in results_children:
		s = {"name": name, "acronym": acronym, "label": type}
		nodes.append(s)
		target = i
		i += 1
		for child_name, child_type in children:
			if child_name is None:
				continue
			print("child :" + child_name)
			c = {"name": child_name, "label": child_type.lower()}
			nodes.append(c)
			source = i
			i += 1
			rels.append({"source": source, "target": target, "caption": "IS_PART_OF"})

	results_parents = graph.run(
		"MATCH (s {struct_name: {name}}) "
		"OPTIONAL MATCH (s)-[r:IS_PART_OF]->(p) "
		"RETURN s.struct_name as name, s.struct_acronym as acronym, labels(s)[0] as type, "
		"collect([p.struct_name, labels(p)[0]]) as parents "
		"LIMIT 1", {"name": name})

	for name, acronym, type, parents in results_parents:
		s = {"name": name, "acronym": acronym, "label": type}
		source = nodes.index(s)
		
		for parent_name, parent_type in parents:
			if parent_name is None:
				continue
			print("parent : " + parent_name)
			p = {"name": parent_name, "label": parent_type.lower()}

			nodes.append(p)
			target = i
			i += 1
			rels.append({"source": source, "target": target, "caption": "IS_PART_OF"})

	print(nodes)
	print(rels)
	return {"nodes": nodes, "links": rels}

if __name__ == "__main__":
    run(port=8080)
