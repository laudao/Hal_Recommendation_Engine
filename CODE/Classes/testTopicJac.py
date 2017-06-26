A = [('a', 0.8), ('b', 0.5), ('c', 0.3)]
B = [('a', 0.5), ('c', 0.8), ('b', 0)]

#for tuple in B:
#	if 'a' in tuple:
#		print(tuple)
print(A)
print(B)

all= []
for tupleA in A:
	a = tupleA[0]
	for tupleB in B:
		if a in tupleB:
			list = [tupleA, tupleB]
			all.append(list)

print(all)
inter = 0
union = 0
for couple in all:
	mini = min(couple[0][1], couple[1][1])
	inter = inter + mini
	maxi = max(couple[0][1], couple[1][1])
	union = union + maxi

print(inter)
print(union)
print(inter/union)

#print((0.5+0.3)/(0.8+0.5+0.8))
#print((0.7+0.4+0.7)/(0.8+0.5+0.8))

