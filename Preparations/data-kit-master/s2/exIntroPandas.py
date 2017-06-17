import pandas as pd
import numpy as np

villes_stades = {'nom':["Paris","Marseille","Lyon","Lens","Toulouse"],'population':[212,80,44,32,39],'zip':["75","13","69","62","31"],'stade':[49691,42000,41842,12097,35472]}
villes_df = pd.DataFrame(villes_stades)

print villes_stades
print villes_df

print villes_df[['nom', 'stade']]
print villes_df.ix[3]

print villes_df[villes_df['stade'] > 30000]
