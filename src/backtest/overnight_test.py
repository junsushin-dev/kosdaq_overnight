import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from scipy.stats import kstest 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# use kolomogorov - smirnov test to check if the given data is normally distributed
def check_normal_dist(data):
	ks_val, p_val = kstest(data, 'norm', (data.mean(), data.std()))
	if p_val > 0.05:
		return True
	else:
		return False

# show results for the overnight strategy
# buys at previous day's close price and sells at today's open price
# prints: cumulated returns, yearly returns
# plots graph: portfolio value under strategy, compared to holding the asset 
def backtest_overnight(file_path, kelly='off', daily_interest=(0.05/252), start_date=False, end_date=False):

	# process date to datetime object and sort the dataframe by index
	df = pd.read_csv(file_path, engine='python')
	df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
	df = df.set_index('date')
	df = df.sort_index()

	# dataframe slicing for start / end dates
	if start_date == False:
		if end_date == False: 
			pass
		else:
			df = df[:end_date]
	else:
		if end_date == False:
			df = df[start_date:]
		else:
			df = df[start_date:end_date]

	# calculate returns and log returns
	df['returns'] = (df['open'] / df['close'].shift(1) - 1).fillna(0)
	df['log_returns'] = (np.log(df['open']) - np.log(df['close'].shift(1))).fillna(0)

	# not using kelly criterion, invest 100% of AUM to the strategy
	if kelly == 'off':
		kelly_criterion = 1

	# if kelly == 'on'
	# calculate optimal kelly criterion

	else: 
		plt.hist(df['log_returns'])
		plt.show()
		print(check_normal_dist(df['log_returns']))

		#kelly_criterion = (df['returns'].mean() - daily_interest) / ( df['returns'].std() ** 2)
		kelly_criterion = 1.7094
		print('optimal leverage: {}'.format(kelly_criterion))

	# make cumulative data for plotting graph
	cumulated_returns = []
	initial_return = 1
	for daily_return in df['returns']:
		delta = daily_return
		if kelly_criterion >= 1:
			initial_return *= (1 + kelly_criterion * delta - (kelly_criterion-1) * daily_interest) * (1 - 0.000046077*2)
		else:
			initial_return *= (1 + kelly_criterion * delta) * (1 - 0.000046077*2)
		cumulated_returns.append(initial_return)

	cumulated_returns = pd.Series(cumulated_returns, index=df.index)

	# show results
	print("max value of portfolio: {}".format(cumulated_returns.max()))
	print("cumulated returns: {}".format(cumulated_returns[-1]))

	total_years = (df.index[-1] - df.index[0]).total_seconds() / datetime.timedelta(days = 365).total_seconds()
	print("yearly returns: {}".format(np.exp(np.log(cumulated_returns[-1])/total_years)))

	print(cumulated_returns*(df['close'].iloc[0]))
	plt.plot(df.index.to_pydatetime(), df['close'], label='original asset')
	plt.plot(df.index.to_pydatetime(), cumulated_returns*(df['close'].iloc[0]), label='overnight_strategy')
	plt.title("Portfolio Value Comparison")
	plt.legend(loc='upper right')
	plt.show()

	return

file_path = r'C:\신준수\프로그래밍\kosdaq_overnight\src\backtest\data\TIGER 코스닥150.csv'
#cumulated_returns = backtest_overnight(file_path, kelly='off', daily_interest=0.035/365)
cumulated_returns = backtest_overnight(file_path, start_date='20190528')