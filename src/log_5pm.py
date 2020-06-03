import check_mkt_open
import logger
import login_test
import win32com.client
import sys

path = r"C:\Users\Administrator\Downloads\kosdaq_overnight\log_data.csv"

if(check_mkt_open.check_today_open() == 0):
	sys.exit()

else:
	app = login_test.login()
	today_logs = logger.get_trade_log_today()
	print(len(today_logs))
	portfolio_value = logger.get_portfolio_value()
	for row in today_logs:
		row.append(portfolio_value)
		logger.write_log(row, path)
	print("Logging Successful")
	login_test.logout()
	sys.exit()
