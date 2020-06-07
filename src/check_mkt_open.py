import sys
import win32com.client
import datetime

holidays_2019 = [20190101, 20190204, 20190205, 20190206, 20190301, 20190501, 20190506, 20190606, 20190815, 20190912, 20190913, 20191003, 20191009, 20191225, 20191231]

# INPUT: date in YYYYMMDD(num) format
# OUTPUT: -1(error) / 0(non-trading day) / 1(trading day) 
def check_if_open(date):
    dt_format = datetime.datetime.strptime(str(date), "%Y%m%d")
    if dt_format.weekday() in [5,6]:
        return 0
    elif dt_format in holidays_2019:
        return 0
    else:
        return 1

def check_today_open():
    now = datetime.datetime.now()
    today_str = now.strftime("%Y%m%d")
    #print(today_str)
    today_ulong = int(today_str)
    #print(today_ulong)
    return check_if_open(today_ulong)

# TEST CASES

# normal open day
# print(check_if_open(20190313))

# holidays
# print(check_if_open(20190301))

# weekends
# print(check_if_open(20190315))

# today
# print(check_today_open())