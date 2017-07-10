#import enchant
#from TopicGraph import *

#toto = ([2, 3, 4], ['a', 'b', 'c'])
#l = [4, 5, 'a']
#
#l = l + toto[0]
#print(l)
#
#toto = [['coucou'],['hello']]
#toto = "Hello coucou ca va ?"
#
#s = "toto"
#print(enchant.Dict("en_US").check("Le"))
#if s == "toto":
#	print("oui")
#tata = toto.split(' ')
#print(tata)
#print(len(tata))
#print(tata[len(tata)-1])
#print(enchant.Dict("en_US").check(tata[len(tata)-1]))

#print(enchant.Dict("en_US").check("Intelligence)"))
#print(toto.split(' ', 1)[len(toto)])

#topic_occ = [0 for i in range(8)]

#for tuple in res:
#	print(tuple[1][0])
#	topic_occ[(tuple[1][0])] += 1

#c = input("> ")
#for i in range(1,4):
#	print(i)

#print(c)
#print(type(c))

l1 = ['a', 'b', 'c', 'd']
l2 = ['b', 'f', 'd', 'h']
ll1 = [0.4, 0.1, 0.3, 0.7]
ll2 = [0.23, 0.5, 0.34, 0.19]

mix1 = sorted(zip(l1, ll1), reverse=True)
print(mix1)
l1 = [word for (word, weight) in mix1]
mix2 = sorted(zip(l2, ll2), reverse=True)
l2 = [word for (word, weight) in mix2]
print(mix2)
print(l1)
print(l2)

#l = list(set().union(l1, l2))
#ll = []
l = []
for tuple1 in mix1:
	w = tuple1[0]
	check = 0
	for tuple2 in mix2:
		if w in tuple2:	
			l.append([tuple1, tuple2])
			check = 1
	if check == 0:
		l.append([tuple1, (w,0.0)])

for tuple2 in mix2:
	w = tuple2[0]
	check = 1
	for couple in l:
		if w in couple[0]:
			check = 0
	if check:
		l.append([tuple2, (w,0.0)])

print(l)

ll = []
lll = []
for couple in l:
#	print(couple)
#	print(couple[0][1])
#	print(couple[1][1])
	maxi = max(couple[0][1], couple[1][1])
	ll.append(maxi)
	lll.append(couple[0][0])

print(ll)
print(lll)

sort = sorted(zip(ll, lll), reverse=True)
print(sort)
words = [word for (weight, word) in sort]
weights = [weight for (weight, word) in sort]
print(words)
print(weights)

words_final = []
weights_final = []
for i in range(0,5):
	words_final.append(words[i])
	weights_final.append(weights[i])

print(words_final)
print(weights_final)
