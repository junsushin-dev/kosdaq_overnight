# by Junsu Shin @ github.com/junsushin-dev

import pandas as pd
import win32com.client
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

asset_code = "A228790"

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

asset_name = instCpCodeMgr.CodeToName(asset_code)
print(asset_name)

def get_price_data_per_day(code, start_date, end_date):

	instStockChart.SetInputValue(0, code)
	instStockChart.SetInputValue(1, ord('2'))
	#instStockChart.SetInputValue(2, start_date)
	#instStockChart.SetInputValue(3, end_date)
	instStockChart.SetInputValue(4, 5000)
	instStockChart.SetInputValue(5, (0,2,3,4,5,8))
	instStockChart.SetInputValue(6, ord('D'))
	instStockChart.SetInputValue(9, ord('1'))

	instStockChart.BlockRequest()

	column_labels = ['open','high','close','low','close','volume']

	numData = instStockChart.getHeaderValue(3)
	numField = instStockChart.getHeaderValue(1)

	for i in range(numField):
		print(type(instStockChart.GetDataValue(i,0)))

	index = pd.Series([instStockChart.GetDataValue(0, i) for i in range(numData)])
	open_price = pd.Series([instStockChart.GetDataValue(1, i) for i in range(numData)])
	high_price = pd.Series([instStockChart.GetDataValue(2, i) for i in range(numData)])
	low_price = pd.Series([instStockChart.GetDataValue(3, i) for i in range(numData)])
	close_price = pd.Series([instStockChart.GetDataValue(4, i) for i in range(numData)])
	volume = pd.Series([instStockChart.GetDataValue(5, i) for i in range(numData)])
	df = pd.DataFrame({'date': index, 'open':open_price, 'high':high_price, 'low':low_price, 'close':close_price, 'volume':volume})
	df = df.set_index('date')

	return df

start_date = 20151001
end_date = 20190201

stock_price_data = get_price_data_per_day(asset_code, start_date, end_date)

print(stock_price_data)

print(dir_path)

output_path = dir_path + "\\" + asset_name + ".csv"
print(output_path)

stock_price_data.to_csv(output_path)
