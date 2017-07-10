import py2neo.ogm
from py2neo.ogm import *
import testGOActor as act

class Movie(GraphObject):
    __primarykey__ = "title"

    title = Property()
    tag_line = Property("tagline")
    released = Property()

    actors = RelatedFrom("act.Actor()", "ACTED_IN")
    directors = RelatedFrom("act.Actor()", "DIRECTED")
    producers = RelatedFrom("act.Actor()", "PRODUCED")

