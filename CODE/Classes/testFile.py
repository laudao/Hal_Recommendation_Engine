import os.path

f = "toto.txt"
print(os.path.isfile(f))

#inp = ""
#while len(inp) == 0:
#	inp = input("> ")
#	if inp == None:
#		print("none")
#print(type(inp))

#f = open("toto.txt", "w")
#i = 3
#f.write(str(i+1))
#f.close()

#f = open("rech.txt", "r")
#print((f.readline())[11])
#f.close()

#f = open("titi.txt", 'w')
#f.write("titi")
#f.write("\n")
#f.write("tutu")
#f.close()
#
#f = open("titi.txt", 'r')
#l = f.readline()[0:-1]
#print(l)
#if l == "titi":
#	print("oui")
#print(f.readline())
#f.close()
#
#f = open("tata.txt", "a")
#
#files = ['re', 're2']
#for filename in files:
#	f.write(filename + "\n")
#
#f = open("topics_info.txt", 'r')
#f.readline()
#print(int((f.readline())[10:-1]))
#f.close()

#f = open('kkkk.txt', 'r+')
#for i in range(1):
#	f.readline()
##	f.write(str(i)+"\n")
#f.write("ici")
#f.close()

with open('numbers.txt') as f:
	lines = f.read().splitlines()

for i in range(len(lines)):
	lines[i] = int(lines[i])

print(lines)
