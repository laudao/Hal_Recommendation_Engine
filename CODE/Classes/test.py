import py2neo.ogm
from py2neo.ogm import *
from py2neo import Graph, authenticate
import test2

# stuff to run always here such as class/def
class Person(GraphObject):
	__primarykey__ = "name"

	name = Property()
	toto = Property()
	likes = RelatedTo("Person", "COUCOU")
	totofriend = RelatedFrom("Person" or "SpecialPerson", "TOTO_FROM")

	def test(GraphObject):
		print("test")


if __name__ == "__main__":
	# this won't be run when imported 
	authenticate("localhost:7474", "neo4j", "stage")
	
	graph = Graph("http://localhost:7474/db/data/")
	print(graph.data("MATCH (a:Person) RETURN a.name, a.born LIMIT 4")) # prints graph
	
	person1 = Person()
	person1.name = "Laura"
	person1.toto = "toto"
	person2 = Person()
	person2.name = "Gaetan"
	person1.likes.add(person2)
	person3 = Person()
	person3.name = "Lea"
	person3.toto = "titi"
	person2.totofriend.add(person1)
	sp = test2.SpecialPerson()
	sp.nom = "blurp"
	sp.toto = "tata"
	person2.totofriend.add(sp)

	graph.push(sp)
	graph.push(person3)
	graph.push(person2)	
	print(graph.data("MATCH (a:Person) RETURN a.name")) # prints graph
	
	print(Person.select(graph, "Gaetan").first())
#	for friend in person1.likes:
#		print(friend.name)
	
#	for toto in person2.totofriend:
#		print(toto)
	
#	person1.test()

