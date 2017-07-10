import progressbar
from time import sleep

#bar = progressbar.ProgressBar()
bar = progressbar.ProgressBar(maxval=20, \
	widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
f = open("my_list", 'w')
my_list = [1, 4, 5, 0]

bar.start()
v=0
for i in bar(my_list):
	f.write(str(i))
	bar.update(v+1)
	sleep(0.1)

#for i in range(20):
 #   bar.update(i+1)
#    sleep(0.1)
#bar.finish()
