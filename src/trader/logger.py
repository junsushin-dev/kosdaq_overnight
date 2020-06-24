from datetime import date
import win32com.client
import csv

# get daily trading log
# returns a list of trade logs performed today
# returns nothing if an error occurs
def get_trade_log_today():
    
    # 연결 여부 체크
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        return
    # check account number
    objTrade =  win32com.client.Dispatch("CpTrade.CpTdUtil")
    initCheck = objTrade.TradeInit(0)
    if (initCheck != 0):
        print("주문 초기화 실패")
        #exit()
    acc = objTrade.AccountNumber[0] #계좌번호
    accFlag = objTrade.GoodsList(acc, 1)  # 주식상품 구분
    print(acc, accFlag[0])

    objCpTd5341 = win32com.client.Dispatch("CpTrade.CpTd5341")

    objCpTd5341.SetInputValue(0, acc) #계좌번호
    objCpTd5341.SetInputValue(1, accFlag[0]) # 주식상품 구분
    objCpTd5341.SetInputValue(4, ord('0')) # 순차적 순서로

    objCpTd5341.BlockRequest()

    num_entry = objCpTd5341.GetHeaderValue(6)
    print(num_entry)

    result = []

    for i in range(num_entry):
        curr_date = date.today()
        asset_code = objCpTd5341.GetDataValue(3, i)
        asset_name = objCpTd5341.GetDataValue(4, i)
        buy_or_sell = objCpTd5341.GetDataValue(24, i) # 1 is sell, 2 is buy
        traded_volume = objCpTd5341.GetDataValue(10, i)
        traded_price = objCpTd5341.GetDataValue(11, i)
        temp_row = [curr_date, asset_code, asset_name, buy_or_sell, traded_volume, traded_price]
        result.append(temp_row)

    return result

# get portfolio value
# returns the value of the portfolio for today
def get_portfolio_value():

    # 연결 여부 체크
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        return

    # check account number
    objTrade =  win32com.client.Dispatch("CpTrade.CpTdUtil")
    initCheck = objTrade.TradeInit(0)
    if (initCheck != 0):
        print("주문 초기화 실패")
        #exit()
    acc = objTrade.AccountNumber[0] #계좌번호
    accFlag = objTrade.GoodsList(acc, 1)  # 주식상품 구분
    print(acc, accFlag[0])

    objCpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

    objCpTd6033.SetInputValue(0, acc)
    objCpTd6033.SetInputValue(1, accFlag[0])
    objCpTd6033.SetInputValue(3, "1") # returns starting from 100%

    objCpTd6033.BlockRequest()

    stock_value = objCpTd6033.GetHeaderValue(3)
    cash_value = objCpTd6033.GetHeaderValue(9)
    portfolio_value = stock_value + cash_value

    return portfolio_value

# write a new row to the log_data file
# data = [date, asset_code, asset_name, buy/sell, traded_volume, traded_price, portfolio_value]
def write_log(data, file_path):
    with open(file_path, 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    csvFile.close()
    return