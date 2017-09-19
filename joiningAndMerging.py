import pandas as pd

df1 = pd.DataFrame({'Year':[2001, 2002, 2003, 2004],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]})

df3 = pd.DataFrame({'Year':[2001, 2003, 2004, 2005],
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53]})

# Merge on one
#print(pd.merge(df1, df2, on='HPI'))

# Merging on multiple
#print(pd.merge(df1, df2, on=['HPI', 'Int_rate']))

# Change the index to HPI for both df1 and df3
#df1.set_index('HPI', inplace=True)
#df3.set_index('HPI', inplace=True)

# Join the two dfs
#joined = df1.join(df3)
#print(joined)


# Merge on year using outer join
# left join = use df1's years
# right join = use df3's years
# inner (default) = join on  matching years -- prevents NaN
# outer = join on all years -- causes NaN
merged = pd.merge(df1, df3, on='Year', how='inner')
merged.set_index('Year', inplace=True)
print(merged)

# merge when index matters, join when it doesn't
# concatenate/append to add/elongate
