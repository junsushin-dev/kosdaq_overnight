import sys
import win32com.client
 
def buy_available_amount():

	# 연결 여부 체크
	objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
	bConnect = objCpCybos.IsConnect
	if (bConnect == 0):
	    print("PLUS가 정상적으로 연결되지 않음. ")
	    exit()
	 
	# 주문 초기화
	objTrade =  win32com.client.Dispatch("CpTrade.CpTdUtil")
	initCheck = objTrade.TradeInit(0)
	if (initCheck != 0):
	    print("주문 초기화 실패")
	    exit()

	# check account number
	acc = objTrade.AccountNumber[0] #계좌번호
	accFlag = objTrade.GoodsList(acc, 1)  # 주식상품 구분
	print(acc, accFlag[0])

	# Check for the amount able to buy
	CpTdNew5331A = win32com.client.Dispatch("CpTrade.CpTdNew5331A")
	CpTdNew5331A.SetInputValue(0, acc)
	CpTdNew5331A.SetInputValue(1, accFlag[0])
	CpTdNew5331A.SetInputValue(2, "A143860")
	CpTdNew5331A.SetInputValue(3, "03")
	CpTdNew5331A.SetInputValue(5, "Y") # 미수 사용하지 않음
	CpTdNew5331A.SetInputValue(6, ord('2'))

	CpTdNew5331A.BlockRequest()
	buy_amount = CpTdNew5331A.GetHeaderValue(13) # A229200은 증거금 40% 종목
	print("buy_amount :{}".format(buy_amount))

	# 주식 매수 주문
	objStockOrder = win32com.client.Dispatch("CpTrade.CpTd0311")
	objStockOrder.SetInputValue(0, "2")   # 2: 매수
	objStockOrder.SetInputValue(1, acc)   #  계좌번호
	objStockOrder.SetInputValue(2, accFlag[0])   # 상품구분 - 주식 상품 중 첫번째
	objStockOrder.SetInputValue(3, "A143860")   # 종목코드 - A003540 - 대신증권 종목
	objStockOrder.SetInputValue(4, buy_amount)   # 매수수량
	objStockOrder.SetInputValue(8, "03")
	 
	# 매수 주문 요청
	ret = objStockOrder.BlockRequest()

	print("Buying Request Successful")

	return