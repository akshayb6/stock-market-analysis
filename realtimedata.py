from yahoo_finance import Share
import datetime
import time
import psycopg2

yahoo = Share('YHOO')
google = Share('GOOGL')
amazon = Share('AMZN')
fb = Share('FB')
apple = Share('AAPL')


stocks = {yahoo:'YHOO',google:'GOOGL',amazon:'AMZN',fb:'FB',apple:'AAPL'}


realtime=str(datetime.datetime.now().time())

conn = psycopg2.connect(database="testdb", user="postgres", password="abc", host="127.0.0.1", port="5432")
cur = conn.cursor()
cur.execute('''DROP TABLE realtime''')
cur.execute('''CREATE TABLE realtime
       (ID SERIAL PRIMARY KEY     NOT NULL,
       Symbol		VARCHAR,
       Time         VARCHAR    NOT NULL,
       Price         REAL     NOT NULL,
       Volume 		BIGINT   
       );''')

while(realtime < '22:00:00.000000'):
	for x in stocks:
		x.refresh()
		name = stocks[x]
		price = x.get_price()
		volume = x.get_volume()
		print name,price,volume,realtime[:-7:]
		cur.execute("INSERT INTO realtime (Symbol,Time,Price,Volume) \
			VALUES (%s,%s,%s,%s)",(name,realtime,price,volume))

	time.sleep(60)
	realtime = str(datetime.datetime.now().time()) 
	# break




conn.commit()
conn.close()
