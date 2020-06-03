import check_mkt_open
import sell_open
import login_test
import sys

if(check_mkt_open.check_today_open() == 0):
	sys.exit()

else:
	app = login_test.login()
	sell_open.sell_available_amount()
	login_test.logout()
	sys.exit()