import quandl
import pandas as pd
import pickle

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
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
            
    print(main_df.head())        

    # Saving the data for later use
    pickle_out = open('us_states.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

# No need to initialize every time if pickling
#grab_initial_state_data()

# Grabbing the serialized data
pickle_in = open('us_states.pickle','rb')
HPI_data = pickle.load(pickle_in)
print(HPI_data)

# Pandas version of pickling
HPI_data.to_pickle('pandas.pickle')
HPI_data2 = pd.read_pickle('pandas.pickle')
print(HPI_data2)
