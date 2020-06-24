import sys
import win32com.client

def sell_available_amount():

    # 연결 여부 체크
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
     
    # 주문 초기화
    objTrade =  win32com.client.Dispatch("CpTrade.CpTdUtil")
    initCheck = objTrade.TradeInit()
    print(initCheck)
    if (initCheck != 0):
        print("주문 초기화 실패")
        exit()

    # check account number
    acc = objTrade.AccountNumber[0] #계좌번호
    accFlag = objTrade.GoodsList(acc, 1)  # 주식상품 구분
    print(acc, accFlag[0])

    # Check for the amount able to buy
    CpTdNew5331B = win32com.client.Dispatch("CpTrade.CpTdNew5331B")
    CpTdNew5331B.SetInputValue(0, acc)
    CpTdNew5331B.SetInputValue(1, accFlag[0])
    CpTdNew5331B.SetInputValue(2, "A143860")
    #CpTdNew5331B.SetInputValue(3, ord("1")) # 주식채권 구분: 주식
    #CpTdNew5331B.SetInputValue(4, ord("1")) # 현금신용대용 구분: 현금
    #CpTdNew5331B.SetInputValue(8, ord("0"))

    CpTdNew5331B.BlockRequest()
    data_num = CpTdNew5331B.GetHeaderValue(0)
    print(data_num)
    sell_amount = CpTdNew5331B.GetDataValue(12, 0)
    print("asset_code: " + CpTdNew5331B.GetDataValue(0, 0))
    print("asset_name: " + CpTdNew5331B.GetDataValue(1, 0))
    print("sell_amount: " + str(sell_amount))

    # 주식 매도 주문
    objStockOrder = win32com.client.Dispatch("CpTrade.CpTd0311")
    objStockOrder.SetInputValue(0, "1")   # 1: 매도
    objStockOrder.SetInputValue(1, acc)   #  계좌번호
    objStockOrder.SetInputValue(2, accFlag[0])   # 상품구분 - 주식 상품 중 첫번째
    objStockOrder.SetInputValue(3, "A143860")   # 종목코드 - A068270 - 셀트리온 종목
    objStockOrder.SetInputValue(4, sell_amount)   # 매도수량 전량
    objStockOrder.SetInputValue(8, "03")

    # 매도 주문 요청
    ret = objStockOrder.BlockRequest()

    print("Selling Request Successful")

    return