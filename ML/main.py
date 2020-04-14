import pandas as pd
import datetime as dt 
from matplotlib import pyplot as plt
from function import main_driver



df = pd.read_csv("cases.csv")
df.drop(['Province/State','Lat', 'Long'],axis=1,inplace=True)
df = df.T
df.columns = df.iloc[0]
df = df.iloc[1:]
#changing the data type
df.index=pd.to_datetime(df.index)
#print(df.head())
main_driver(df.loc[:,'Belgium'].astype(float),[[("2020-3-13","2020-4-2")],[("2020-2-1","2020-3-13")]])
