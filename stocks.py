import requests
import json
from datetime import datetime
import datetime
import time
import pymysql
import sys

mysql_pw = sys.argv[1]
apikey = sys.argv[2]

conn = pymysql.connect(
  host='80.219.242.46',
  port=3306,
  user="colab",
  passwd=mysql_pw,
  db="finance")

#dates = []
dates = [str(datetime.date.today() - datetime.timedelta(days=1))] # Running for yesterday (default case)
#dates = ['2020-03-25', '2020-03-26', '2020-03-27'] # Manual backfill for specific dates

#for i in range(7, 30): # Backfilling a range of dates
#  dates.append(str(datetime.date.today() - datetime.timedelta(days=i)))

URL_FOREX_TIME_SERIES = 'Time Series FX (Daily)'
URL_OPEN_PRICE = '1. open'
URL_HIGH_PRICE = '2. high'
URL_CLOSE_PRICE = '4. close'
URL_LOW_PRICE = '3. low'
URL_TRADING_VOLUME = '5. volume'

def fNumFloatForex(string):
    return round(float(string), 4)

def fNumFloat(string):
    return round(float(string), 2)

def fNumInt(string):
    return round(float(string), 2)

usd_to_eur = 1.2
eur_to_cad = 0.9

do_forex = True
do_stocks = True
do_portfolio = True

for j in range(len(dates)):
  query_date = dates[j]
  print("Running for date: "+query_date)

  if(do_forex):
    forex_pairs = [['USD', 'EUR'],
                  ['USD', 'CHF'],
                  ['USD', 'CAD'],
                  ['EUR', 'CHF'],
                  ['EUR', 'CAD'],
                  ['CHF', 'CAD']]

    length = len(forex_pairs)

    for i in range(length): #range(0, 1): 
      url = "https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=%s&to_symbol=%s&apikey=%s" % (forex_pairs[i][0], forex_pairs[i][1], apikey)
      myResponse = requests.get(url)
      
      try:
        jData = json.loads(myResponse.content) 
        data = jData[URL_FOREX_TIME_SERIES][query_date];
        
        if(myResponse.ok):
          
          from_curr = forex_pairs[i][0]
          to_curr = forex_pairs[i][1]

          open_price = fNumFloatForex(data[URL_OPEN_PRICE])
          high_price = fNumFloatForex(data[URL_HIGH_PRICE])
          low_price = fNumFloatForex(data[URL_LOW_PRICE])
          close_price = fNumFloatForex(data[URL_CLOSE_PRICE])
          high_low_spread = fNumFloatForex(high_price - low_price)
          open_close_spread = fNumFloatForex(open_price - close_price)
          timestamp = int(time.mktime(datetime.datetime.strptime(query_date, "%Y-%m-%d").timetuple()))
          
          param = (timestamp, str(query_date), str(from_curr), str(to_curr), open_price, close_price, low_price, high_price, high_low_spread, open_close_spread)
          insert = "INSERT INTO forex (timestamp, date, from_currency, to_currency, open_price, close_price, low_price, high_price, high_low_spread, open_close_spread) VALUES (%s,'%s','%s','%s',%s,%s,%s,%s,%s,%s)" % param
          print("Inserting Forex pair into table 'forex': ("+from_curr+","+to_curr+")")
          
          cur = conn.cursor()
          cur.execute(insert)
          conn.commit()

          if(from_curr == 'USD' and to_curr == 'EUR'):
            usd_to_eur = close_price
            #print("USD to EUR: " + str(usd_to_eur))
          
          if(from_curr == 'EUR' and to_curr == 'CAD'):
            eur_to_cad = close_price
            #print("EUR to CAD: " + str(eur_to_cad))

      except  KeyError:
        print("Key not found: Probably no values at given date")

      time.sleep(20)

  # End do_forex

  if(do_stocks):
    URL_STOCK_TIME_SERIES = 'Time Series (Daily)'

    stocks = [['AMZN', 'USD', 10],
              ['BABA', 'USD', 50],
              ['BIDU', 'USD', 10],
              ['BTAI', 'USD', 100],
              ['CLDR', 'USD', 100],
              ['FB', 'USD', 25],
              ['GOOG','USD',  68],
              ['IMAE.AMS', 'EUR', 200],
              ['IUSA.AMS', 'EUR', 955],
              ['JD', 'USD', 80],
              ['LYFT', 'USD', 30],
              ['NKL', 'CAD', 432],
              ['NVIV', 'USD', 66],
              ['VOO', 'USD', 333],
              ['VWO', 'USD', 100],
              ['VEA', 'USD', 0]]

    length = len(stocks)
    total_value = float(0)

    for i in range(length): #Only do 2 iterations to not run into rate limiting errors
      url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&outputsize=compact" % (stocks[i][0], apikey)
      myResponse = requests.get(url)

      try:
        jData = json.loads(myResponse.content)
        data = jData[URL_STOCK_TIME_SERIES][query_date];
      
        if(myResponse.ok and data is not None):
          timestamp = int(time.mktime(datetime.datetime.strptime(query_date, "%Y-%m-%d").timetuple()))
          symbol = stocks[i][0]
          currency = stocks[i][1]
          num_stocks = stocks[i][2]
          trading_volume = fNumInt(data[URL_TRADING_VOLUME])
          
          orig_open_price = fNumFloat(data[URL_OPEN_PRICE])
          orig_high_price = fNumFloat(data[URL_HIGH_PRICE])
          orig_low_price = fNumFloat(data[URL_LOW_PRICE])
          orig_close_price = fNumFloat(data[URL_CLOSE_PRICE])
          orig_open_close_spread = fNumFloat(orig_open_price - orig_close_price)
          orig_high_low_spread = fNumFloat(high_price - low_price)
          orig_symbol_value = num_stocks * orig_close_price
          orig_open_close_symbol_spread = num_stocks * orig_open_close_spread
          orig_high_low_symbol_spread = num_stocks * orig_high_low_spread
          
          #open_price = orig_open_price
          #high_price = orig_high_price
          #low_price = orig_low_price
          #close_price = orig_close_price
          #symbol_value = orig_symbol_value
          #high_low_spread = orig_high_low_spread
          #open_close_spread = orig_open_close_spread
          #open_close_symbol_spread = orig_open_close_symbol_spread
          #high_low_symbol_spread = orig_high_low_symbol_spread
          
          rate = 1
        
          if(currency=='USD'):
            rate = usd_to_eur
            print("Converting USD to EUR at rate: " + str(rate))

          if(currency=='CAD'):
            rate = 1/eur_to_cad
            print("Converting CAD to EUR at rate: " + str(rate))

          symbol_value = fNumFloat(orig_symbol_value * rate)
          open_price = fNumFloat(orig_open_price * rate)
          high_price = fNumFloat(orig_high_price * rate)
          low_price = fNumFloat(orig_low_price * rate)
          close_price = fNumFloat(orig_close_price * rate)
          open_close_spread = fNumFloat(open_price - close_price)
          high_low_spread = fNumFloat(high_price - low_price)
          open_close_symbol_spread = fNumFloat(num_stocks * open_close_spread)
          high_low_symbol_spread = fNumFloat(num_stocks * high_low_spread)

          #print("Orig. O/C spread"+str(orig_open_close_spread))
          #print("Orig. O/C symbol spread"+str(orig_open_close_symbol_spread))
          #print("O/C spread"+str(open_close_spread))
          #print("O/C symnbol spread"+str(open_close_symbol_spread))

          param = (timestamp, query_date, symbol, currency, orig_open_price, orig_close_price, orig_low_price, orig_high_price, orig_high_low_spread, orig_open_close_spread, open_price, close_price, low_price, high_price, high_low_spread, open_close_spread, trading_volume)
          insert = "INSERT INTO stocks (timestamp, date, symbol, currency, orig_open_price, orig_close_price, orig_low_price, orig_high_price, orig_high_low_spread, orig_open_close_spread, open_price, close_price, low_price, high_price, high_low_spread, open_close_spread, trading_volume) VALUES (%s,'%s','%s','%s',%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)" % param
          print("Inserting symbol into table 'stocks': " + symbol)

          cur = conn.cursor()
          cur.execute(insert)
          conn.commit()

          if(do_portfolio and num_stocks > 0):
            param = (timestamp, query_date, symbol, num_stocks, currency, orig_symbol_value, symbol_value, orig_open_close_symbol_spread, open_close_symbol_spread, orig_high_low_symbol_spread, high_low_symbol_spread)
            insert = "INSERT INTO portfolio (timestamp, date, symbol, num_stocks, currency, orig_symbol_value, symbol_value, orig_open_close_spread, open_close_spread, orig_high_low_spread, high_low_spread) VALUES (%s, '%s', '%s', %s, '%s', %s, %s, %s, %s, %s, %s)" % param
            print("Inserting symbol into table 'portfolio': " + symbol)
            cur = conn.cursor()
            cur.execute(insert)
            conn.commit()
        else:
          myResponse.raise_for_status()
      except  KeyError:
        print("Key not found: Probably no values at given date")
      time.sleep(20)
  # End do_stocks
#End j loop
