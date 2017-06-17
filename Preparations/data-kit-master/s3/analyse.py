from TwitterSearch import *
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime

twitter_api = TwitterSearch(
    consumer_key = 'RmFscwclpvdjPSaGjS4aoPV1a',
    consumer_secret = 'hOWpBILNUqcUsCdFBgSVP8ZQcDIVFIS2vLpY7ifBxmXqKS3jgF',
    access_token = '3405596541-ougG4SZWbcHeS3ef0sCJIO3WVu5RAOFAZzVyh5t',
    access_token_secret = 'CbJj75tF3yJgRyVVTrTgDf8w397Bg2tM2mcxZHrQJ0CPn'
    )

tso = TwitterSearchOrder() # creation d'un objet TwitterSearchOrder()
tso.set_keywords(['Elysee']) # la recherche s'effectue sur Elysee 
search_results = twitter_api.search_tweets(tso) # recherche tous les tweets correspondant
#print search_results
#print 'type(search_results) : ', type(search_results) # dict de dict de liste de dict
#print search_results.keys()
#print 'type(search_results[\'content\']) : ', type(search_results['content']) # dict
#print search_results['content'].keys()
#print 'type(search_results[\'content\'][\'statuses\']) : ', type(search_results['content']['statuses']) # liste
#print len(search_results['content']['statuses']) # nombre de tweets qu'on peut recuperer
#print 'type(search_results[\'content\'][\'statuses\'][99]) : ',type(search_results['content']['statuses'][99]) # dict
#print search_results['content']['statuses'][99].keys() 
#print search_results['content']['statuses'][99]['text']

# analyse de l'integralite des tweets du compte de l'Elysee
tuo = TwitterUserOrder('Elysee')
elysee_results = twitter_api.search_tweets(tuo) # recherche tweets correspondants
#print elysee_results['content'][0]['text']

elysee = json.load(open('data/elysee.txt')) # liste de dict
#print "taille du fichier : ", len(elysee)
#print elysee[0]['text']

colonnes = ['text', 'retweet_count', 'created_at']
elysee_df = pd.DataFrame(elysee, columns=colonnes) # creation du data frame
date = pd.to_datetime(elysee_df['created_at']) # colonne created_at transformee en serie temporelle
#print elysee_df
elysee_df = elysee_df.set_index(date)
print elysee_df.head()
count_date = elysee_df['text'].resample('W').count()
count_date.plot().set_title('Nombre de tweets du compte @Elysee par semaine')
plt.show()
