from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
app = Flask(__name__)
import os
import time
import random
import redis

r = redis.Redis(
    host ='redis-10386.c10.us-east-1-3.ec2.cloud.redislabs.com',
    port = 10386,
	password = 'HsaYFXRlXaKVKLaQcALVFqLnp3XfyHYV')
#conn = sqlite3.connect('database.db')
# print("Opened database successfully")
#conn.execute('drop table earthquake')
#conn.execute('CREATE TABLE Earthquake (time text,latitude real,longitude real,depth real,mag real,magType text,nst real,gap real,dmin real,rms real,net text,id text,updated text,place text,type text,horizontalError real,depthError real,magError real,magNst real,status text,locationSource text,magSource text)')
# print("Table created successfully")
# conn.close()

port = int(os.getenv('PORT', 8000))
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def upload_csv():
   return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)	  
       con.close()
       return render_template("result.html",msg = "Record inserted successfully")
	   
@app.route('/list')
def list():
   con = sql.connect("database.db")
 
   
   cur = con.cursor()
   cur.execute("select * from Earthquake")
   
   rows = cur.fetchall();
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/records')
def records():
   return render_template('records.html')
   
@app.route('/options' , methods = ['POST', 'GET'])
def options():
   con = sql.connect("database.db")
   #mc = memcache.Client(['127.0.0.1:11211'], debug=0)
   start_time = time.time()
   num =int(request.form['num'])
   rows = []
   c = []
   for i in range(num):
       val = round(random.uniform(2,5),1)
       cur = con.cursor()
       a = 'select * from Earthquake WHERE mag = '+str(val)
       cur.execute("select * from Earthquake WHERE mag = ?" ,(val,))
       get = cur.fetchall();
       rows.append(get)
       v = str(val)
       if r.get(a):
	       print ('Cached')
           #c.append(var)
       else:
           print('Not Cached')
		   #c.append(var)
           cur.execute("select * from Earthquake WHERE mag = ?" ,(val,))
           get = cur.fetchall();
           r.set(a,get)		   
   con.close()
   end_time = time.time()
   elapsed_time = end_time - start_time
   return render_template("list1.html",rows = [rows,elapsed_time])
	   
@app.route('/restricted')
def restricted():
   return render_template('rest.html')
   
@app.route('/options2' , methods = ['POST', 'GET'])
def options2():
   con = sql.connect("database.db")
   start_time = time.time()	   
   num =int(request.form['num'])
   loc = (request.form['loc'])
   rows = []
   for i in range(num):
       cur = con.cursor()
       b = 'select * from Earthquake WHERE place LIKE ?', ('%'+loc+'%',)
       cur.execute("select * from Earthquake WHERE place LIKE ?", ('%'+loc+'%',))
       get = cur.fetchall();
       rows.append(get)
       if r.get(b):
	       print ('Cached')
       else:
           print('Not Cached')
           cur.execute("select * from Earthquake WHERE place LIKE ?", ('%'+loc+'%',))
           get = cur.fetchall();
           r.set(b,get) 		   
   con.close()
   end_time = time.time()
   elapsed_time = end_time - start_time
   return render_template("list2.html",rows = [rows,elapsed_time])
	

   
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port,debug = True)
