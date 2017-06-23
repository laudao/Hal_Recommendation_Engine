import urllib as ur
import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np
import py2neo.ogm
from py2neo.ogm import *
from py2neo import Graph, authenticate
from test import Person

authenticate("localhost:7474", "neo4j", "stage")

graph = Graph("http://localhost:7474/db/data/")

struct = "Conception et Test de Systèmes MICroélectroniques"
urlStruct = "https://api.archives-ouvertes.fr/ref/structure/?q=name_s:" + '"' + struct + '"' + "&fl=docid type_s parentType_s parentDocid_i"
#url="https://api.archives-ouvertes.fr/ref/author/?q=structure_s:" + '"' + struct + '"' + "&fl=docid fullName_s structureId_i structure_s"
url="https://api.archives-ouvertes.fr/search/?q=structName_s:" + '"' + struct + '"' +"&fl=docid authFullName_s authStructId_i"
print(url)
#url = 'https://api.archives-ouvertes.fr/search/?fq=rteamStructAcronym_s:"MLIA"&fl=docid authFullName_s rteamStructId_i rteamStructName_s rteamStructAcronym_s rteamStructCountry_s labStructAcronym_s title_s'
r = requests.get(urlStruct) # response object
# print(type(r.text)) # str
#print(type(r.json())) # => responses object converted to dict

dicjson = r.json()
#print(dicjson.keys()) # response
#print(type(dicjson['response'])) # dict
#print(dicjson['response'].keys()) # start, numFound, docs
#print(type(dicjson['response']['docs'])) # list
#print(dicjson['response']['docs'])
#print(type(dicjson['response']['docs'][0])) # dict
#print(dicjson['response']['docs'][0].keys())
#print(type(dicjson['response']['docs'][0]['authFullName_s'])) # list
#print(type(dicjson['response']['docs'][0]['authFullName_s'][0])) # list
#print(dicjson['response']['docs'][0]['rteamStructId_i']) 

df = pd.DataFrame(dicjson['response']['docs'])
#struct_df = dicjson['response']['docs'][0]
#type_struct = struct_df['type_s'] # type de structure
#
#if (type_struct == "researchteam" or type_struct == "department"):
#	while (struct_df['parentType_s'] != "laboratory" or struct_df['parentType_s'] != "institution"):
#		urlStructParent = "https://api.archives-ouvertes.fr/ref/structure/?q=docid:" + '"' + struct_df['parentDocid_i'] + '"' + "&fl=docid type_s parentType_s parentDocid_i" 
#		r2 = requests.get(urlStructParent)
#		dicjson2 = r2.json()
#		df2 = pd.DataFrame(dicjson2['response']['docs'])
#	

df.set_index([df['docid']],drop=True, append=False, inplace=True, verify_integrity=False)
df = df.drop('docid', axis=1)
print(df.head())

""" build list of team members """

Bojan = Person()

print(df.iloc[0])
#name = df['authFullName_s'].ix[1306311][0]
#Bojan.name = name

#graph.push(Bojan)
#print(graph.data("MATCH (a:Person) RETURN a.name")) # prints graph
#Bojan.test()
