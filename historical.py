import psycopg2
from yahoo_finance import Share
#yahoo = Share('GOOG')
company_list=['GOOG','YHOO','AMZN','AAPL','FB']
li=[]
for i in range(len(company_list)):
	comp=Share(company_list[i])
	li.append(comp.get_historical('2014-04-25', '2015-04-25'))

print li[1][1]
#comp=Share(company_list[1])
#li.append(comp.get_historical('2014-04-25', '2015-04-25'))

conn = psycopg2.connect(database="testdb", user="postgres", password="abc", host="127.0.0.1", port="5432")
cur = conn.cursor()
cur.execute('''DROP TABLE hist2''')
cur.execute('''CREATE TABLE hist2
       (ID SERIAL PRIMARY KEY     NOT NULL,
       Symbol		VARCHAR,
       Time         DATE    NOT NULL,
       Open         REAL     NOT NULL,
       Close        REAL,
       High         REAL,
       Low          REAL,
       Volume 		BIGINT   
       );''')

#print len(li[i])
for i in range(5):
	for j in range(len(li[i])):
		cur.execute("INSERT INTO hist2 (Symbol,Time,Open,Close,High,Low,Volume) \
			VALUES (%s,%s,%s,%s,%s,%s,%s)",(li[i][j]['Symbol'],li[i][j]['Date'],li[i][j]['Open'],li[i][j]['Close'],li[i][j]['High'],li[i][j]['Low'],li[i][j]['Volume']))
cur.execute('''COPY (SELECT * FROM hist2 WHERE Symbol='YHOO') TO '/home/akshay/software_csv/yhoo_hist.csv' DELIMITER ',' CSV HEADER;''')
cur.execute('''COPY (SELECT * FROM hist2 WHERE Symbol='AAPL') TO '/home/akshay/software_csv/aapl_hist.csv' DELIMITER ',' CSV HEADER;''')
cur.execute('''COPY (SELECT * FROM hist2 WHERE Symbol='GOOG') TO '/home/akshay/software_csv/goog_hist.csv' DELIMITER ',' CSV HEADER;''')
cur.execute('''COPY (SELECT * FROM hist2 WHERE Symbol='FB') TO '/home/akshay/software_csv/fb_hist.csv' DELIMITER ',' CSV HEADER;''')
cur.execute('''COPY (SELECT * FROM hist2 WHERE Symbol='AMZN') TO '/home/akshay/software_csv/amzn_hist.csv' DELIMITER ',' CSV HEADER;''')
conn.commit()
conn.close()


