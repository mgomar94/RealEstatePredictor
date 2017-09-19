import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np

web_stats = {'Day':[1,2,3,4,5,6],
             'Visitors':[43,53,34,45,64,34],
             'Bounce_Rate':[65,72,62,64,54,66]}

df = pd.DataFrame(web_stats)

# Visualizing the dataframe
#print(df)
#print(df.head())
#print(df.tail())
#print(df.tail(2))


# Setting the index returns a df, does not alter original df
#print(df.set_index('Day'))
#print(df.head())


# Possible solution
#df = df.set_index('Day')
#print(df.head())


# Better solution
#df.set_index('Day', inplace=True)
#print(df.head())


# Referencing columns
# Second line cannot handle variables with spaces (Bounce Rate vs Bounce_Rate)
#print(df['Visitors'])
#print(df.Visitors) 


# Reference two columns
#print(df[['Bounce_Rate','Visitors']])


# Convert to list/array
#print(df.Visitors.tolist())
#print(np.array(df[['Bounce_Rate','Visitors']]))


# Back to df
df2 = pd.DataFrame(np.array(df[['Bounce_Rate','Visitors']]))
print(df2)



