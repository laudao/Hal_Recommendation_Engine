# -*- coding: utf-8 -*-
# file name: class-ModelLDA
# author: Michelle MALARA
# creation date: 15\ 06\ 2017

from class_PageHal import PageHAL
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from gensim import corpora, models
import pyLDAvis.gensim
import pprint

class ModelLDA:
	def __init__(self, page, nb_topics, nb_passe, nb_word):
		self.page = page
		self.corpus = '*#*'
		self.language = page.language
		self.nb_topics = nb_topics
		self.nb_passe = nb_passe
		self.nb_word = nb_word

	@property
	def page(self):
		return self.__page

	@property
	def corpus(self):
		return self.__corpus
	
	@property
	def language(self):
		return self.page.language
	
	@property
	def nb_topics(self):
		return self.__nb_topics
	
	@property
	def nb_passe(self):
		return self.__nb_passe
	
	@property
	def nb_word(self):
		return self.__nb_word
	
	@page.setter
	def page(self, x):
		if type(x) == PageHAL:
			self.__page = x
			try:
				self.corpus = "#*#"
			except AttributeError:
				pass
		else:
			print("type of", x, "must be PageHAL")
	
	@corpus.setter
	def corpus(self, x):
		if x == "*#*":
			ext = self.page.extract()
			if len(ext) == 0:
				print("ici")
				ext = self.page.extract_title()
				if len(ext) == 0:
					print("The corpus is empty you must modify the page")
				else:
					print("Warning the corpus contains only the titles")
			self.__corpus = ext
		elif x == "#*#":
			pass
		else:
			print("You cant modify the corpus")
	
	@language.setter
	def language(self, x):
		self.page.language = x
	
	@nb_topics.setter
	def nb_topics(self, x):
		if type(x) == int and x > 0:
			self.__nb_topics = x
		else:
			print('nb_topics must be a positive integer.', x, 'is not.')
	
	@nb_passe.setter
	def nb_passe(self, x):
		if type(x) == int and x > 0:
			self.__nb_passe = x
		else:
			print('nb_passe must be a positive integer.', x, 'is not.')
	
	@nb_word.setter
	def nb_word(self, x):
		if type(x) == int and x > 0:
			self.__nb_word = x
		else:
			print('nb_word must be a positive integer.', x, 'is not.')
	
	@staticmethod
	def clean_text_en(doc, punctuation, lemma):
		words_stop = set(stopwords.words('english'))
		parasit_word = "des pour two using nous ont une les fair par sur dans que moi plus non aux cette est one".split()
		for w in parasit_word:
			words_stop.add(w)
		stop_free = " ".join([i for i in doc.lower().split() if not(i in words_stop)])  # enlever les mots inutile
		punc_free = ''.join(ch for ch in stop_free if not(ch in punctuation))  # enlever la ponctuation
		normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())  # associ un lemne aux mots (dogs -> dog)
		res = []
		for w in normalized.split():
			if len(w) > 4:
				res.append(w)
		return res
	
	@staticmethod
	def clean_text_fr(doc, punctuation, lemma):
		words_stop_fr = set(stopwords.words('french'))
		parasit_word = "plus using two cette cet qui pour cela les d'un afin ainsi ils avon d'un the and".split()
		for w in parasit_word:
			words_stop_fr.add(w)
		punc_free = ''
		for ch in doc:
			if ch not in punctuation:
				punc_free += ch
			else:
				punc_free += ' '
		normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())  # associ un lemne a un mot (dogs -> dog)
		stop_free = " ".join([i for i in normalized.lower().split() if i not in words_stop_fr])  # on enlève les mots inutile
		res = []
		for w in stop_free.split():
			if len(w) > 2:
				res.append(w)
		return res
	
	def normalize_corpus(self):
		punctuation = set(string.punctuation)  # ponctuation
		lemma = WordNetLemmatizer()
		if self.language == 'en':
			res = [ModelLDA.clean_text_en(t, punctuation, lemma) for (d, t) in self.corpus]
		else:
			res = [ModelLDA.clean_text_fr(t, punctuation, lemma) for (d, t) in self.corpus]
#		print("res" + str(type(res)))
		return res
		
	def extract_lda_topics(self):
		all_doc = self.normalize_corpus()
		dictionary = corpora.Dictionary(all_doc)  # Creating dictionary (object) of corpus : term (unique) indexed
		matrix = [dictionary.doc2bow(doc) for doc in all_doc]  # matrix[j]=(i,o) o=occurrence word i(index dic) in doc j
		lda = models.ldamodel.LdaModel  # Creating object for LDA model
		ldamodel = lda(matrix, num_topics=self.nb_topics, id2word=dictionary, passes=self.nb_passe)
		return ldamodel, matrix, dictionary
	
	def visualisation(self):
		if not self.corpus:
			print("The corpus is empty. Calculating topics is impossible...")
		else:
			ldamodel, doc_term_matrix, dictionary = self.extract_lda_topics()
			visu = pyLDAvis.gensim.prepare(ldamodel, doc_term_matrix, dictionary, R=self.nb_word)
			pyLDAvis.show(visu)
	
	def print_topic(self):
		if not self.corpus:
		    print("The corpus is empty. Calculating topics is impossible...")
		else:
			ldamodel, doc_term_matrix, dictionary = self.extract_lda_topics()
			x = ldamodel.print_topics(num_topics=self.nb_topics, num_words=self.nb_word)  # recover topics
			pprint.pprint(x)

#filename = "rech.txt"
#page = PageHAL.create_page_file(filename)
##print()
#
#obj = ModelLDA(page, 8, 40, 5)
#ldamodel, doc_term_matrix, dic = obj.extract_lda_topics()
#print(ldamodel)
#print(ldamodel.show_topics(formatted=False))
#ex = ['PRIMARY', 'OBJECTIVES:', 'Awake', 'surgeries', 'of', 'slow-growing', 'tumours', 'invading', 'the', 'brain', 'and', 'guided', 'by', 'direct', 'electrical', 'stimulation', 'induce', 'major', 'brain', 'reorganizations', 'accompanied', 'with', 'slight', 'impairments', 'post-operatively.', 'In', 'most', 'cases,', 'these', 'deficits', 'are', 'so', 'slight', 'after', 'a', 'few', 'days', 'that', 'they', 'are', 'often', 'not', 'detectable', 'on', 'classical', 'neuropsychological', 'evaluations.', 'Consequently,', 'this', 'study', 'investigated', 'whether', 'simple', 'visuo-manual', 'reaction', 'time', 'paradigms', 'would', 'sign', 'some', 'level', 'of', 'functional', 'asymmetries', 'between', 'both', 'hemispheres.', 'Importantly,', 'the', 'visual', 'stimulus', 'was', 'located', 'in', 'the', 'saggital', 'plane', 'in', 'order', 'to', 'limit', 'attentional', 'biases', 'and', 'to', 'focus', 'mainly', 'on', 'the', 'inter-hemispheric', 'asymmetry.', 'METHODS', 'AND', 'PROCEDURES:', 'Three', 'patients', '(aged', '41,', '59', 'and', '59', 'years)', 'after', 'resections', 'in', 'parietal', 'regions', 'and', 'a', 'control', 'group', '(age\u2009=\u200944,', 'SD\u2009=\u20096.9)', 'were', 'compared', 'during', 'simple', 'uni-', 'and', 'bimanual', 'reaction', 'times', '(RTs).', 'MAIN', 'OUTCOMES', 'AND', 'RESULTS:', 'Longer', 'RTs', 'were', 'observed', 'for', 'the', 'contralesional', 'compared', 'to', 'the', 'ipsilesional', 'hand', 'in', 'the', 'unimanual', 'condition.', 'This', 'asymmetry', 'was', 'reversed', 'for', 'the', 'bimanual', 'condition', 'despite', 'longer', 'RTs.', 'CONCLUSION', 'AND', 'CLINICAL', 'IMPLICATIONS:', 'Reaction', 'time', 'paradigms', 'are', 'useful', 'in', 'these', 'patients', 'to', 'monitor', 'more', 'precisely', 'their', 'functional', 'deficits,', 'especially', 'their', 'level', 'of', 'functional', 'asymmetry,', 'and', 'to', 'understand', 'brain', '(re)organization', 'following', 'slow-growing', 'lesions.']

#bow = ldamodel.id2word.doc2bow(ex)
#print(len(bow))
#doc_topics, word_topics, phi_values = ldamodel.get_document_topics(bow, per_word_topics=True)
#print(bow)
#print(word_topics)
#print(doc_topics)

#print(type(ldamodel))
#print(type(doc_term_matrix))
#print(type(dic))
#print(dic)
#print(doc_term_matrix)
#obj.print_topic()
#obj.visualisation()
#
#obj.language = "fr"
#
#print(obj.language)
#obj.print_topics()
#obj.visualisation()
