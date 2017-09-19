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
ax1 = plt.subplot2grid((2,1), (0,0))

# Create a second subplot below the first, but share the same x axis
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

# Plotting the correlation between Texas and Alaska
TX_AK_12corr = pd.rolling_corr(HPI_data['TX'], HPI_data['AK'], 12)
HPI_data['TX'].plot(ax=ax1, label='TX HPI')
HPI_data['AK'].plot(ax=ax1, label='AK HPI')
ax1.legend(loc=4)
TX_AK_12corr.plot(ax=ax2, label='TX_AK_12_corr')


### Rolling average using a window size of 12
##HPI_data['TX12MA'] = pd.rolling_mean(HPI_data['TX'], 12)
##
### Rolling standard deviation
##HPI_data['TX12STD'] = pd.rolling_std(HPI_data['TX'], 12)
##
##print(HPI_data[['TX', 'TX12MA', 'TX12STD']].head())
##HPI_data[['TX', 'TX12MA']].plot(ax = ax1)
##HPI_data['TX12STD'].plot(ax=ax2)

plt.legend(loc=4)
plt.show()



