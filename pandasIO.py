import pandas as pd

### Convert from csv to df
##df = pd.read_csv('ZILLOW-C4519_ZHVITT.csv')
##
### Set the date as the index
##df.set_index('Date', inplace=True)
##
### Convert the df to a csv and save it locally
##df.to_csv('newcsv2.csv')
##
### Read it in to double check, but notice that index is lost
##df = pd.read_csv('newcsv2.csv')
##
### Read it in, but specify index this time
##df = pd.read_csv('newcsv2.csv', index_col=0)
##
### Name the columns
##df.columns = ['Austin_HPI']
##
### Save it to see the header
##df.to_csv('newcsv3.csv')
##
### Save it without headers
##df.to_csv('newcsv4.csv', header=False)
##
### Read in a csv without header, add header and set index
##df = pd.read_csv('newcsv4.csv', names=['Date', 'Austin_HPI'], index_col=0)
##
### Save as html
##df.to_html('example.html')

# How to rename a column
df = pd.read_csv('newcsv4.csv', names=['Date', 'Austin_HPI'])
df.rename(columns={'Austin_HPI':'77006_HPI'}, inplace=True)

print(df.head())
