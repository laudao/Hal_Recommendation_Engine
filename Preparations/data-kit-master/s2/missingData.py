import pandas as pd
import numpy as np
from numpy import nan as NA

df_null = pd.DataFrame([[1,3,5,8],[5,NA,7,3],[NA,NA,NA,NA],[NA,7,3,2]])
print df_null
print df_null.dropna()
print df_null.dropna(axis=1)
print df_null.dropna(axis=0, how='all')
print df_null.fillna(0)
print df_null.fillna({1:0,2:3})
df_null.fillna(0, inplace=True)
print df_null
