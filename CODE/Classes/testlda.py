from gensim import corpora, models, similarities
from class_ModelLDA import ModelLDA
import json

model = models.LdaModel.load('lda.model')
topics_list = model.show_topics(formatted=False)
print(topics_list)

f = open('topic_language.txt', 'r')
l = f.readline()
print(l)
if l == 'en':
	print('oui')

#f = open('topics_list.txt', 'w')

#for tuple in topics_list:
#	f.write(' '.join(str(s) for s in tuple) + '\n')



