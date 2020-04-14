import pymysql
import pandas as pd

mysql_user = sys.argv[1]
mysql_pw = sys.argv[2]
mysql_db = sys.argv[3]

conn = pymysql.connect(
    host='80.219.242.46',
    port=3306,
    user=mysql_user,
    passwd=mysql_pw,
    db=mysql_db)

query = ('CREATE TABLE forex ('
         'id int(10) AUTO_INCREMENT PRIMARY KEY NOT NULL, '
         'timestamp INT(10) NOT NULL, '
         'date VARCHAR(10) NOT NULL, '
         'from_currency VARCHAR(3) NOT NULL, '
         'to_currency VARCHAR(3) NOT NULL, '
         'open_price FLOAT(10) NOT NULL,  '
         'close_price FLOAT(10) NOT NULL, '
         'low_price FLOAT(10) NOT NULL, '
         'high_price FLOAT(10) NOT NULL, '
         'high_low_spread FLOAT(10) NOT NULL, '
         'open_close_spread FLOAT(10) NOT NULL)')

print (query)

cur = conn.cursor()
cur.execute(query)
conn.commit()

query = ('CREATE TABLE stocks ('
         'id int(10) AUTO_INCREMENT PRIMARY KEY NOT NULL, '
         'timestamp INT(10) NOT NULL, '
         'date VARCHAR(10) NOT NULL, '
         'symbol VARCHAR(10) NOT NULL, '
         'currency VARCHAR(3) NOT NULL, '
         'orig_open_price FLOAT(10) NOT NULL, '
         'orig_close_price FLOAT(10) NOT NULL, '
         'orig_low_price FLOAT(10) NOT NULL, '
         'orig_high_price FLOAT(10) NOT NULL, '
         'orig_high_low_spread FLOAT(10) NOT NULL, '
         'orig_open_close_spread FLOAT(10) NOT NULL, '
         'open_price FLOAT(10) NOT NULL, '
         'close_price FLOAT(10) NOT NULL, '
         'low_price FLOAT(10) NOT NULL, '
         'high_price FLOAT(10) NOT NULL, '
         'high_low_spread FLOAT(10) NOT NULL, '
         'open_close_spread FLOAT(10) NOT NULL, '
         'trading_volume INT(10) NOT NULL)')

print(query)

cur = conn.cursor()
cur.execute(query)
conn.commit()

query = ('CREATE TABLE portfolio ('
         'id int(10) AUTO_INCREMENT PRIMARY KEY NOT NULL, '
         'timestamp INT(10) NOT NULL, '
         'date VARCHAR(10) NOT NULL, '
         'symbol VARCHAR(10) NOT NULL, '
         'currency VARCHAR(3) NOT NULL, '
         'num_stocks INT(10) NOT NULL, '
         'orig_symbol_value FLOAT(10) NOT NULL, '
         'symbol_value FLOAT(10) NOT NULL, '
         'orig_open_close_symbol_spread FLOAT(10) NOT NULL, ' 
         'open_close_symbol_spread FLOAT(10) NOT NULL, ' 
         'orig_high_low_symbol_spread FLOAT(10) NOT NULL, ' 
         'high_low_symbol_spread)')

print (query)

cur = conn.cursor()
cur.execute(query)
conn.commit()
