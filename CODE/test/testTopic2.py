from gensim.corpora import Dictionary
from gensim.models import ldamodel
import numpy as np

texts = [['bank','river','shore','water'],
        ['river','water','flow','fast','tree'],
        ['bank','water','fall','flow'],
        ['bank','bank','water','rain','river'],
        ['river','water','mud','tree'],
        ['money','transaction','bank','finance'],
        ['bank','borrow','money'],
        ['bank','finance'],
        ['finance','money','sell','bank'],
        ['borrow','sell'],
        ['bank','loan','sell']]

dictionary = Dictionary(texts)
print(dictionary.keys())
corpus = [dictionary.doc2bow(text) for text in texts]

np.random.seed(1)
model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=2)

print(model.show_topics())

bow_water = ['bank','water','bank']
bow = model.id2word.doc2bow(bow_water)
doc_topics, word_topics, phi_values = model.get_document_topics(bow, per_word_topics=True)

print(word_topics)
