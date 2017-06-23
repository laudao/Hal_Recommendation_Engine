import py2neo.ogm
from py2neo.ogm import *
import testGOMovie as mv

class Actor(GraphObject):
    __primarykey__ = "name"

    name = Property()
    born = Property()

    acted_in = RelatedTo(mv.Movie())
    directed = RelatedTo(mv.Movie())
    produced = RelatedTo(mv.Movie())
