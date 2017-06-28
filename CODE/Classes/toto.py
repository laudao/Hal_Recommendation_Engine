import enchant
toto = ([2, 3, 4], ['a', 'b', 'c'])
l = [4, 5, 'a']

l = l + toto[0]
print(l)

toto = [['coucou'],['hello']]
toto = "Hello coucou ca va ?"

toto = "In the present work, we investigate real numbers whose sequence of partial quotients enjoys some combinatorial properties involving the notion of palindrome. We provide three new transendence criteria, that apply to a broad class of continued fraction expansions, including expansions with unbounded partial quotients. Their proofs heavily depend on the Schmidt Subspace Theorem."
tata = toto.split(' ')
print(tata)
print(len(tata))
print(tata[len(tata)-1])
print(enchant.Dict("en_US").check(tata[len(tata)-1]))

print(enchant.Dict("en_US").check("superspace"))
#print(toto.split(' ', 1)[len(toto)])
