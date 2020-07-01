# Backtest Module Documentation

### Writer: 신준수

## get_price_data.py

### 설명

지정된 종목코드에 대한 일별 OHLC(Open, High, Low, Close) 가격 데이터를 Creon API를 통해 가져와 csv파일로 저장한다.  

### 1. function -  get_price_data_per_day(code, start_date, end_date):
- Input:
  - code - 종목코드(string)
  - start_date - 시작일자 yyyyMMdd 형식(int)
  - end_date - 종료일자 yyyyMMDD 형식(int)
- Output:
  - df - pandas DataFrame
- Actions:
  - Creon API 연결이 되있는 상태에서 작동
  - 일자, 시가, 고가, 저가, 종가, 거래량 데이터 조회
  - pandas DataFrame을 구성하여 return

~~~
asset_code = "A228790"
start_date = 20151001
end_date = 20190201

stock_price_data = get_price_data_per_day(asset_code, start_date, end_date)
~~~

## overnight_test.py

### 1. function -  check_normal_dist(data):
- Input:
  - data - pandas DataFrame
- Output:
  - True of False - bool
- Actions:
  - kolomogorov - smirnov 테스트를 통하여 주어진 데이터가 정규분포를 따르는지 체크한다.

### 2. function -  backtest_overnight(file_path, kelly='off', daily_interest=(0.05/252), start_date=False, end_date=False):
- Input:
  - file_path - 테스트 대상 csv 데이터 경로 String
  - kelly - 'on' or 'off' String
  - daily_interest - 일일 이자율과 거래비용 double
  - start_date - 테스트 시작일자 False or DateTime
  - end_date - 테스트 종료일자 False or DateTime
- Output: none
- Actions:
  - 주어진 데이터에 대해서 overnight 전략의 백테스팅을 수행하여 기간에 따른 포트폴리오 가치를 그래프로 출력한다
  - kelly가 'on' 일 경우 최적의 켈리비율을 가정한 백테스트를 수행한다
  - kelly가 'off' 일 경우 레버리지 없이 백테스트를 수행한다
  - 포트폴리오 최고가치, 누적 수익률, 연간 수익률을 print 한다

~~~
file_path = r'C:\프로그래밍\kosdaq_overnight\src\backtest\data\TIGER 코스닥150.csv'

backtest_overnight(file_path, start_date='20190528')
~~~
