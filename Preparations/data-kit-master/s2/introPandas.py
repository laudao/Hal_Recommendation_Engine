import pandas as pd
import numpy as np

#ser = pd.Series([1,-2,3,"a"])
#print type(ser)
#print ser.index
#print ser.values
#print ser * 2
#print ser[ser > 0]

#villes = {"Lyon":44,"Marseille":80,"Paris":212,"Toulouse":39}
#ser_villes = pd.Series(villes)
#print ser_villes
#
#zip = ['69','13','75','31']
#ser_villes.index = zip
#print ser_villes

villes = {'nom':["Paris","Marseille","Lyon","Toulouse"],'population':[212,80,44,39],'zip':["75","13","69","31"]}
print villes
villes_df = pd.DataFrame(villes, columns=['nom', 'population'], index = [1,2,3,4])
print villes_df
print villes_df['nom']
print villes_df.ix[3]
villes_df['dette'] = np.arange(1,5)*1000
print villes_df

villes_df2 = villes_df.reindex([1,3,5])
print villes_df2
villes_df2 = villes_df2.fillna(0)
print villes_df2

print villes_df.index
print villes_df.columns
villes_df = villes_df.drop(2, axis=0)
print villes_df



