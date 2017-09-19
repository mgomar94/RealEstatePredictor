import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

# To avoid directly listing api on file
api_key = open('quandlapikey.txt', 'r').read().rstrip()

# Read in html page -- This is a list
def state_list():
    us_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return us_states[0][0][1:]

# Grab each abbrievation and combine them into a single df
def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()
    
    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        df = quandl.get(query, authtoken=api_key)
        df.rename(columns={'Value':str(abbv)}, inplace=True)
        #df = df.pct_change()
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0

        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
            
    print(main_df.head())        

    # Saving the data for later use
    pickle_out = open('us_states3.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

# Grabbing official US HPI data
def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
    return df

# No need to initialize every time if pickling
#grab_initial_state_data()

HPI_data = pd.read_pickle('us_states3.pickle')

# Plotting using matplotlib
fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))

# Resampling data from monthly to annually -- mean is default
HPI_data['TX1yr'] = HPI_data['TX'].resample('A', how='mean')


################ HOW TO HANDLE MISSING DATA #################

# Ignore the missing data -- run regularly
print(HPI_data[['TX', 'TX1yr']].head())

# Remove the NaN
#HPI_data.dropna(inplace=True)
#print(HPI_data[['TX', 'TX1yr']].head())

# Dropping the NaN but only rows with all NaN
#HPI_data.dropna(how='all', inplace=True)
#print(HPI_data[['TX', 'TX1yr']].head())

# Threshold -- drop only if it exceeds threshold of NaN
#Not present

# Filling data -- Forward fill
#HPI_data.fillna(method='ffill', inplace=True)
#print(HPI_data[['TX', 'TX1yr']].head())

# Filling data -- Backward fill
#HPI_data.fillna(method='bfill', inplace=True)
#print(HPI_data[['TX', 'TX1yr']].head())

# Filling data with a specific value
#HPI_data.fillna(value=-99999, inplace=True)
#print(HPI_data[['TX', 'TX1yr']].head())

# Limiting the amount to fill data
HPI_data.fillna(value=-99999, limit=10, inplace=True)
print(HPI_data[['TX', 'TX1yr']].head())

# Calculate how many NaN's exist
print(HPI_data.isnull().values.sum())

HPI_data[['TX', 'TX1yr']].plot(ax = ax1)
plt.legend(loc=4)
plt.show()



