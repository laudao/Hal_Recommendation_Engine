words1 = ['a', 'b', 'c']
weights1 = [0.8, 0.5, 0.3]
words2 = ['a', 'c']
weights2 = [0.5, 0.8]
l1 = []
l2 = []

for word, weight in zip(words1, weights1):
	l1.append((word, weight))

for word, weight in zip(words2, weights2):
	l2.append((word, weight))

print(l1)
print(l2)

all = []
for tuple1 in l1:
	w = tuple1[0]
	check=0
	for tuple2 in l2:
		if w in tuple2:
			all.append([tuple1, tuple2])
			check=1
	if check==0:
		all.append([tuple1, (w, 0.0)])

print(all)

inter=0
union=0
for couple in all:
	print(couple[0][1], couple[1][1])
	mini = min(couple[0][1], couple[1][1])
	inter = inter + mini
	maxi = max(couple[0][1], couple[1][1])
	union = union + maxi

print(inter)
print(union)
print(inter/union)

t1 = Topic(200, words1, weights1)
t2 = Topic(201, words2, weights2)

