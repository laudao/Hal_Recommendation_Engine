import py2neo.ogm
from py2neo.ogm import *
from py2neo import Graph, authenticate


class SpecialPerson(GraphObject):
	__primarykey__ = "nom"

	toto = Property()
	nom = Property()

	totofriend = RelatedTo("Person", "TOTO_TO")

