import quandl
import pandas as pd


# To avoid directly listing api on file
#api_key = open('quandlapikey.txt', 'r').read().rstrip()

# Grab Alaska's API data
#df = quandl.get('FMAC/HPI_AK', authtoken=api_key)
#print(df.head())

# Read in html page -- This is a list
us_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

# Grab only the US States table -- This is a datafram
#print(us_states[0])

# Grab the abbrievations -- This is a column
#print(us_states[0][0])

# Create the tags to easily grab HPI data for each state using the abbrievations
for abbv in us_states[0][0][1:]:
    print("FMAC/HPI_" + str(abbv))


