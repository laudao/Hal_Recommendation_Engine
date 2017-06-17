#!/usr/bin/python2.6
# -*- coding: ISO-8859-1 -*- 

import pandas as pd
import numpy as np
# -*- coding: ISO-8859-1 -*- 
reserve = pd.read_csv("data/reserve.csv")

partis = reserve['Subvention allouée'].groupby(reserve['Groupe politique du parlementaire'])

#print partis
#print partis.sum()
#print partis.count()

#print reserve.sort_values(['Subvention allouée', 'Coût du projet'], ascending=False).head(1)
#
#print reserve['Subvention allouée'].groupby(reserve['Parlementaire transmetteur']).count().sort_values(ascending=False)
#
#print reserve['Subvention allouée'].groupby(reserve['Parlementaire transmetteur']).sum().sort_values(ascending=False)
#
#print reserve['Subvention allouée'].groupby(reserve['Département']).count().sort_values(ascending=False)
#
chambres = reserve['Subvention allouée'].groupby([reserve['Groupe politique du parlementaire'], reserve['Nature']]).count()
#print chambres
#
groupe_chambres = chambres.unstack()
#print groupe_chambres
#print reserve.groupby('Nature').count()

#print reserve['Coût du projet'].groupby(reserve['Nature']).mean()
#print reserve.groupby([reserve['Département'],reserve['Nature']]).size().unstack().ix['YVELINES']
#print reserve[reserve['Bénéficiaire'] == 'PARIS']['Subvention allouée']

mapping = {'CRC':'Partis de Gauche',
           'CRC-SPG':'Partis de Gauche',
           'ECO':'Ecologistes',
           'GDR':'Radicaux',
           'NC':'Centristes',
           'NI':'Non Inscrits',
           'RDSE':'Radicaux',
           'SOC':'Parti Socialiste',
           'SOCV':'Parti Socialiste',
           'SRC':'Parti Socialiste',
           'UC':'Centristes',
           'UDI':'Centristes',
           'UMP':'Union Mouvement Populaire'}
#print groupe_chambres

#print groupe_chambres.groupby(mapping, axis=0).sum()

reserve['parti'] = reserve['Groupe politique du parlementaire'].map(mapping)
#print reserve.head(2)

# 1) Part subventionnee des projets par parti politique 
def part(df):
	return np.mean(df['Subvention allouée']/df['Coût du projet'])

print reserve.groupby('parti').apply(part).sort_values(ascending=False)

# 2)parlementaire, ayant réalisé plus de 50 subventions, qui a le plus de subventions dans sa région
# colonne match permet de verifier si la subvention a ete realisee dans le departement du parlementaire
reserve['match'] = reserve['Département Parlementaire'] == reserve['Département']
# groupby sur match et Parlementaire transmetteur, reduction avec size (compter le nombre de subventions dans departement et hors departement pour chaque parlementaire) puis unstack pour recup DF
sub_parlementaire = reserve.groupby(['Parlementaire transmetteur','match']).size().unstack().fillna(0)
print sub_parlementaire
# colonne total donne nombre total de subventions pour chaque parlementaire 
sub_parlementaire['total'] = sub_parlementaire[True] + sub_parlementaire[False]
# on filtre pour avoir parlementaires ayant realise plus de 50 subventions et on sort pour avoir le premier
print sub_parlementaire[sub_parlementaire['total'] > 50].sort_values(True,ascending=False)

sub_groupe = reserve.groupby(['Groupe politique du parlementaire','match']).size().unstack().fillna(0)
print sub_groupe.sort_values(True,ascending=False)
