import pandas as pd
import numpy as np

villes_stades = {'nom':["Paris","Marseille","Lyon","Lens","Toulouse"],
          'population':[212,80,44,32,39],
          'stade':[49691,42000,41842,12097,35472]}

print villes_stades
villes_df = pd.DataFrame(villes_stades, columns=['population', 'stade'], index = villes_stades['nom'])
print villes_df

def dif(x):
	return x - x.mean()

villes_df_dif = villes_df.apply(dif)
print villes_df_dif['stade']
