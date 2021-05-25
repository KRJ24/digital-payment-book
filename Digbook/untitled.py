from flask import Flask, render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app =Flask(__name__)
app.secret_key = 'a'

app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "MPcGxl6SmL"#user name for remotemysql
app.config['MYSQL_PASSWORD'] = "6CnjrdO2Mi"#password fro remotemysql
app.config['MYSQL_DB'] = "MPcGxl6SmL"#database name in remotemysql
mysql = MySQL(app)

@app.route('/')
def homer():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port = 8080)