import check_mkt_open
import buy_close
import login_test
import sys

if(check_mkt_open.check_today_open() == 0):
	sys.exit()

else:
	app = login_test.login()
	buy_close.buy_available_amount()
	login_test.logout()
	sys.exit()