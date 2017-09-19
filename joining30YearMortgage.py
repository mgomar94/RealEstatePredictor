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
    df.rename(columns={'Value':'United States'}, inplace=True)
    return df

# Pull in the mortgage data from Quandl
def mortgage_30year():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
    #df = df.resample('D')
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df



def supply_data():
    df = quandl.get("FRED/MSACSR", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'Supply'}, inplace=True)
    df = df['Supply']
    return df

def gdp_data():
    df = quandl.get("FRED/MKTGDPUSA646NWDB", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.fillna(method='bfill', inplace=True)
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df

def us_unemployment():
    df = quandl.get("FRED/NROUST", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    df.rename(columns={'Value':'Unemployment Rate'}, inplace=True)
    df = df['Unemployment Rate']
    return df


supply = supply_data()
US_GDP = gdp_data()
US_unemployment = us_unemployment()
m30 = mortgage_30year()
HPI_data = pd.read_pickle('us_states3.pickle')
HPI_bench = HPI_Benchmark()
HPI = HPI_data.join([HPI_bench, m30, US_unemployment, US_GDP, supply])
HPI.dropna(inplace=True)
print(HPI)
print(HPI.corr())

HPI.to_pickle('HPI.pickle')



