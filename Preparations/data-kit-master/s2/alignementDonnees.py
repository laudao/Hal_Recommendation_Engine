import pandas as pd
import numpy as np

villes1_df = pd.DataFrame(np.arange(9).reshape(3,3), columns=['population','dette','zip'], index=['Paris', 'Marseille', 'Lyon'])

villes2_df = pd.DataFrame(np.arange(12).reshape(4,3), columns=['population','zip','budget'], index=['Paris','Nantes','Toulouse','Lyon'])

print villes1_df
print villes2_df
print villes1_df + villes2_df
print villes2_df.add(villes1_df, fill_value=0)
