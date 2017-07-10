l1 = ['toto', 'titi', 'tata', 'tutu']
l2 = [33, 34, 35, 34]

l1bis = [v1 for i, v1 in enumerate(l1) if l2[i] == 34]
l2bis = [v2 for v2 in l2 if v2 == 34]

print(l1bis)
print(l2bis)

for v1, v2 in zip(l1, l2):
	print(v1,v2)
