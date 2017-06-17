import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.random.randn(4,3),columns=['population','zip','budget'],
                       index=['Paris','Nantes','Toulouse','Lyon'])
print df1

print df1.sort_index(axis=0)
print df1.sort_index(axis=1)
print df1.sort_values('population', ascending=False)
print df1.describe()
print df1.count()
