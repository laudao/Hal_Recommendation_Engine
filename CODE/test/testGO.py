import py2neo.ogm
from py2neo.ogm import *
from py2neo import Graph, authenticate

class Movie(GraphObject):
    __primarykey__ = "title"

    title = Property()
    tag_line = Property("tagline")
    released = Property()

    actors = RelatedFrom("Actor", "ACTED_IN")
    directors = RelatedFrom("Actor", "DIRECTED")
    producers = RelatedFrom("Actor", "PRODUCED")


class Actor(GraphObject):
    __primarykey__ = "name"

    name = Property()
    born = Property()

    acted_in = RelatedTo(Movie)
    directed = RelatedTo(Movie)
    produced = RelatedTo(Movie)

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")

m = Movie()
m.title = "Matrix"
a = Actor()
a.name = "Keanu Reeves"
a.acted_in.add(m)
m.actors.add(a)
graph.push(a)

print(Actor.select(graph, "Keanu Reeves").first())
