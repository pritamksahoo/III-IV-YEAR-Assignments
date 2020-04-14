import math
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime as dt 
import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from scipy.special import boxcox, inv_boxcox
from scipy import stats

def milestone_capture(df):
    k = 0
    Cases=[1,10,100,500,1000,2500,5000,10000,20000,40000,60000,100000,120000,200000]
    date_milestone=[]
    for ind in df.index: 
      
      # if df[ind] >= Cases[k]:
      #   k = k + 1
        if df[ind] >= Cases[k]:
            k = k+1
            
        date_milestone.append((ind,df[ind]))
        
    dates = []
    cases = []
    for obj in date_milestone:
        dates.append(obj[0])
        cases.append(obj[1])
    
    dates.append(df.index[-1])
    cases.append(df.iloc[-1])
    df_new = pd.DataFrame({"cases":cases},index=dates)
    df_new.index=pd.to_datetime(df_new.index)
    #df_new = df_new.iloc[1:]
    return df_new

def get_predicted_value(data,diff,params,seasonality):
	if seasonality == True:
		if diff == 0:
			mod = SARIMAX(data,order=params[0],seasonal_order=params[2])
			results = mod.fit()
			forecast = results.get_forecast(steps=1)
			val =forecast.predicted_mean 
			op = val.iloc[0]
		elif diff == 1:
			df_diff = data.diff().dropna()
			mod = SARIMAX(df_diff,order=params[0],seasonal_order=params[2])
			results = mod.fit()
			forecast = results.get_forecast(steps=1)
			val =forecast.predicted_mean
			val = val + data.iloc[-1,0] 
			op = val.iloc[0]
		else:
			df_diff = data.diff(2).dropna()
			df_sig_diff = data.diff().dropna()
			mod = SARIMAX(df_diff,order=params[0],seasonal_order=params[2])
			results = mod.fit()
			forecast = results.get_forecast(steps=1)
			val =forecast.predicted_mean
			op2 = val + data.iloc[-1,0] + df_sig_diff.iloc[-1,0]
			op= op2.iloc[0]
	else :
		if diff == 0:
			mod = SARIMAX(data,order=params[0])
			results = mod.fit()
			forecast = results.get_forecast(steps=1)
			val =forecast.predicted_mean 
			op = val.iloc[0]
		elif diff == 1:
			df_diff = data.diff().dropna()
			mod = SARIMAX(df_diff,order=params[0])
			results = mod.fit()
			forecast = results.get_forecast(steps=1)
			val = forecast.predicted_mean
			val = val + data.iloc[-1] 
			op = val.iloc[0]
		else:
			df_diff = data.diff(2).dropna()
			df_sig_diff = data.diff().dropna()
			mod = SARIMAX(df_diff,order=params[0])
			results = mod.fit()
			forecast = results.get_forecast(steps=1)
			val =forecast.predicted_mean
			op2 = val + data.iloc[-1] + df_sig_diff.iloc[-1]
			op= op2.iloc[0]

	return op


def Sort_Tuple(tup):    
	# getting length of list of tuples 
	lst = len(tup)  
	for i in range(0, lst):  
		  
		for j in range(0, lst-i-1):  
			if (tup[j][1] > tup[j + 1][1]):  
				temp = tup[j]  
				tup[j]= tup[j + 1]  
				tup[j + 1]= temp  
	return tup

def get_model(data,seasonality):
	output = []
	p = q = range(0, 3)
	d = range(0,1)
	pdq = list(itertools.product(p, d, q))
	
	if seasonality == True:
		seasonal_pdq = [(x[0], x[1], x[2], 7) for x in list(itertools.product(p, d, q))]
		for param in pdq:
			for param_seasonal in seasonal_pdq:
				try:
					mod = SARIMAX(data,order=param,seasonal_order=param_seasonal,enforce_stationarity=False,enforce_invertibility=False)
					results = mod.fit()
					if math.isnan(results.aic):
						output.append((param,10000,param_seasonal))
					else:
						output.append((param,results.aic,param_seasonal))
				except: 
					continue
	else:
		
		for param in pdq:
			try:
				mod = SARIMAX(data, order=param)
				results = mod.fit()
				if math.isnan(results.aic):
					output.append((param,10000))
					
				else:
					output.append((param,results.aic))
			except: 
					continue

	output = Sort_Tuple(output)
	return(output[0])
def get_best_model(data,diff_needed,seasonality):
	if diff_needed == 0:
		best_model = get_model(data,seasonality)
	elif diff_needed == 1:
		df_diff = data.diff().dropna()
		best_model = get_model(df_diff,seasonality)
	else :
		df_diff = data.diff(2).dropna()
		best_model = get_model(df_diff,seasonality)

	return best_model

def check_stationarity(data):
	results = adfuller(data)
	Pvalue = float(results[1])
	if Pvalue <= 0.06:
		return True
	else:
		return False

def driver(data,seasonality=False):

	#Checking the data for stationarity
	diff_needed = None   
	if check_stationarity(data) == True:
		diff_needed = 0
	else :
		df_diff = data.diff().dropna()
		if check_stationarity(df_diff) == True:
			diff_needed = 1
		else:
			diff_needed = 2
	
	model_params = get_best_model(data,diff_needed,seasonality)
	print("Dekhhhhhhhh!!!!")
	print(diff_needed)
	print(model_params)
	value = get_predicted_value(data,diff_needed,model_params,seasonality)
	return value


def Any_series(df,date_list):
	values=[]
	for obj in date_list:
		start_date = obj[0]
		end_date = obj[1]
		values.append(df[start_date:end_date])
	dates = []
	val = []
	for sublist in values:
		for ind in sublist.to_frame().index:
			dates.append(ind)
			val.append(df[ind])
	df_new = pd.DataFrame({'cases':val},index=dates)
	df_new.index=pd.to_datetime(df_new.index)
	return df_new

def backup(data):
	fit1 = Holt(data).fit(smoothing_level=0.8, smoothing_slope=0.2, optimized=False)
	fcast1 = fit1.forecast(1).rename("Holt's linear trend")
	return fcast1

def reciprocal_tranfromation(df):
	lmd = [-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0]
	res_lmd = None
	lowest_p = 0.05
	diff_needed = 0
	#x = stats.boxcox(df.loc[:,'cases'], lmbda=-0.5)
	print(df)
	for l in lmd:
		try:

			df['cases'] = stats.boxcox(df.loc[:,'cases'], lmbda=l)
			series = df.loc[:,'cases']		
			result1 = adfuller(series)
			#print(results[1])
			series = df.loc[:,'cases'].diff(1).dropna()
			result2 = adfuller(series)
			#print(result[1])
			series = df.loc[:,'cases'].diff(2).dropna()
			result3 = adfuller(series)
			df['cases'] = inv_boxcox(df['cases'],l)

			if result1[1] <= lowest_p:
				lowest_p = results[1]
				res_lmd = l
			elif result2[1] <= lowest_p:
				lowest_p = result2[1]
				res_lmd = l
				diff_needed = 1
			elif result3[1] <= lowest_p:
				lowest_p = result3[1]
				res_lmd = l
				diff_needed = 2
			else :
				print("foo")
		except:
			continue
		

	return (res_lmd,diff_needed)
	


def main_driver(data_org,dates_list):
	seasonality = False
	base_value = driver(data_org)
	# df_milestone = milestone_capture(data)
	# trend_value = driver(df_milestone)
	# if math.isnan(trend_value):
	# 	trend_value = backup(df_milestone)
	# print(trend_value)
	

	# LOCKDOWN
	lockdown_values = None
	list_lockdown_dates = dates_list[0]
	df_lockdown = Any_series(data_org,list_lockdown_dates)
	lmb, diff = reciprocal_tranfromation(df_lockdown)
	if lmb is None:
		lockdown_values = backup(df_norm)
	else:
		df_lockdown['cases'] = stats.boxcox(df_lockdown.loc[:,'cases'], lmbda=lmb)
		diff_needed = diff
		data = df_lockdown['cases']
		model_params = get_best_model(data,diff_needed,seasonality)
		value = get_predicted_value(data,diff_needed,model_params,seasonality)
		lockdown_values = inv_boxcox(value,lmb)
	

	# NO LOCKDOWN
	no_lockdown_values = None
	list_no_lockdown_dates = dates_list[1]
	df_nl = Any_series(data_org,list_no_lockdown_dates)
	#df_nl = df_nl[df_nl['cases'] >= 75]
	#print(df_nl)

	# Scaling
	series = data_org.iloc[-13:]
	lower, upper = series.min(), series.max()
	df_nl=(df_nl-df_nl.min())/(df_nl.max()-df_nl.min())
	df_norm = lower + (upper - lower) * df_nl
	#print(df_norm)


	lmb, diff = reciprocal_tranfromation(df_norm)
	print(lmb,diff)
	if lmb is None:
		no_lockdown_values = backup(df_norm)


	else:
		df_norm['cases'] = stats.boxcox(df_norm.loc[:,'cases'], lmbda=lmb)
		diff_needed = diff
		data = df_norm['cases']
		model_params = get_best_model(data,diff_needed,seasonality)
		value = get_predicted_value(data,diff_needed,model_params,seasonality)
		no_lockdown_values = inv_boxcox(value,lmb)

	print(no_lockdown_values)
	print(lockdown_values)
	print(data_org.tail(2))
	print(base_value)	