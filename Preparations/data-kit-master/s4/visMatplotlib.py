import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

p = pd.DataFrame(np.random.randn(100,1))
#print p
#p.plot()

# on parse le dataset et on utilise la colonne 1 (dates) comme index
coffee = pd.read_csv("data/coffee_shop.csv", 
                     parse_dates = True, 
                     index_col=1)
#print coffee.head(3)

# affiche l'evolution des ventes par mois 
coffee_s = coffee['Sales'].groupby(coffee.index).sum()
#coffee_s.plot()
# xlim et ylim fixent les limites des axes, kind='area' rend une aire plutot qu'une ligne
#coffee_s.plot(ylim=[0,40000],kind='area')

# afficher l'evolution des ventes et de la marge par mois 
grouped_sm = coffee[['Sales','Margin']].groupby(coffee.index).sum()
#grouped_sm.plot(ylim=[0,40000])
#grouped_sm.plot(title='Evolution des ventes et de la marge, Coffee Shop, 2012 - 2013')

### Exercice ###
## Evolution mensuelle de la marge et des depenses ##
grouped_md = coffee[['Margin', 'Total Expenses']].groupby(coffee.index).sum()
#grouped_md.plot()
# ou
#coffee[['Margin','Total Expenses']].resample('M').sum().plot()

## Evolution trimestrielle du profit ##
#coffee['Profit'].resample('Q').mean().plot()

###

## afficher le nombre de ventes par marche ##
grouped_m = coffee['Sales'].groupby(coffee['Market']).sum()
#grouped_m.plot(kind='bar')
#grouped_m.plot(kind='barh')

## denombrer le nombre d'occurences de chacun des produits ##
#coffee['Product'].value_counts().plot(kind='barh')

## afficher la part des Major/Small markets au sein de chacun des Market
coffee_mm = coffee['Sales'].groupby([coffee['Market'], coffee['Market Size']]).sum()
#print coffee_mm.head()
# coffee_mm.plot(kind='barh') # une ligne par combinaison d'index
## On fait pivoter le graphe ##
#print coffee_mm.unstack().head()
#coffee_mm.unstack().plot(kind='barh')

## empiler chacun de ces graphes
#coffee_mm.unstack().plot(kind='barh', stacked=True)

### Exercice : - Creez un graphe en baton affichant la part des ventes, des Espresso ou des Coffee par type (Decaf ou Regular) ###

coffee_ex = coffee['Sales'].groupby([coffee['Product Type'], coffee['Type']]).sum()
def part(x):
    return 100*x/float(x.sum())

group_part = coffee_ex.groupby(level=0).apply(part)
#group_part.unstack().plot(kind='barh',stacked=True)

df = pd.DataFrame(np.random.rand(100,2))
## Tracer un nuage de points ##
#df.plot(kind='scatter',x=0,y=1)

### Faire un nuage de points des produits par moyenne de ventes et marges mensuelles ###
#coffee[['Sales', 'Margin']].groupby(coffee['Product']).mean().plot(kind='scatter',x='Sales',y='Margin')
###


plt.show()
