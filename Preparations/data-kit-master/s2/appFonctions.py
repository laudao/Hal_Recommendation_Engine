import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.random.randn(4,3),columns=['population','zip','budget'],
                   index=['Paris','Nantes','Toulouse','Lyon'])
print df1

f = lambda x: x.max() - x.min()

print df1.apply(f, axis=0)
print df1.apply(f, axis=1)
