from GraphObjects import *

l = [(0, [('system', 0.012609257797263372), ('algorithm', 0.010559382827702302), ('problem', 0.0093634238118058318), ('network', 0.0079789220069335851), ('polynomial', 0.0061057581142717112), ('solution', 0.0052864758969646828), ('based', 0.0049825788062838614), ('using', 0.0049089086330868364), ('new', 0.0048617286383334062), ('solving', 0.0042805675285063367)]), (1, [('system', 0.012015897784127632), ('approach', 0.0080435790722740378), ('order', 0.0077718162844308478), ('agent', 0.0063369760151455526), ('network', 0.0059960660901519991), ('distributed', 0.0059459007601725166), ('paper', 0.0058329366376959312), ('propose', 0.0045027276016752658), ('based', 0.0042696172455264358), ('algorithm', 0.0039215739264348553)]), (2, [('network', 0.0085560204986363988), ('model', 0.0069656448414894259), ('data', 0.0068329685434285452), ('algorithm', 0.0061131144787431903), ('paper', 0.0058114431224270107), ('strategy', 0.0047770734739725883), ('process', 0.004427279648805957), ('based', 0.0044157287911420753), ('different', 0.0043142402938297006), ('result', 0.004259282176435797)])]

authenticate("localhost:7474", "neo4j", "stage")
graph = Graph("http://localhost:7474/db/data/")
words = []
weight = []

#for obj in l:
#	num.append(obj[0])
#	for couple in obj[1]:
#		words.append(couple[0])
#		weight.append(couple[1])

for topic in l:
	words = []
	weight = []
	for couple in topic[1]:
		words.append(couple[0])
		weight.append(couple[1])
	t = Topic(topic[0], words, weight)
	graph.push(t)
	print(words)
	print(weight)

#print(Topic.select(graph, 0)).first()
rt = ResearchTeam.select(graph, 388262).first()
print(rt.struct_name)

