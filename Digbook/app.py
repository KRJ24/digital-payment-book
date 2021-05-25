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
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']


        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for applying registring at smartinterns """
            message  = 'Subject: {}\n\n{}'.format("smartinterns Carrers", TEXT)
            #sendmail(TEXT,email)
            #sendgridmail(email,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/login',methods =['GET','POST'])
def login():
    global userid
    msg = ''


    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid =  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'

            msg = 'Logged in successfully !'
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT date,payable,payed,pending FROM userd WHERE username = % s ', (username,))
            account = cursor.fetchall()
            colnames=['Date of purchase    ','Payable amount   ','Payed amount   ','Pending Payment   ']
            return render_template('display.html', msg = msg,account=account,colnames=colnames,username=username)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg,)

@app.route('/loginadmin',methods =['GET', 'POST'])
def loginadmin():
    global userid
    msg = ''


    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userad WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'

            msg = 'Logged in successfully !'
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT username,date,payable,payed,pending FROM userd')
            account = cursor.fetchall()
            colnames=['Username','Last date of purchase    ','Payable amount   ','Payed amount   ','Pending Payment   ']
            return render_template('admindash.html', msg = msg,account=account,colnames=colnames)
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginadmin.html', msg = msg)

@app.route('/display')
def display():


        print(session["username"],session['id'])
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userd WHERE  = %s', (str(session['username'])))
        data= cursor.fetcall()
        print("datadisplay",data = data)

    
        return render_template('display.html', data = data)

@app.route('/logout')

def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')

@app.route('/complaint',methods =['GET', 'POST'])
def complaint():
    msg=''
    if request.method == 'POST' :
        complaint=request.form['complaint']
        date=request.form['date']
        username=request.form['username']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO complaint VALUES (NULL, % s, % s,% s)', (username,date,complaint))
        mysql.connection.commit()
        msg = 'Complaint successfully registered !'
    return render_template('complaint.html',msg=msg)

@app.route('/admindash')
def dashboard():

    return render_template('admindash.html')

@app.route('/newpurchase',methods =['GET', 'POST'])
def newpurchase():
    msg=''
    if request.method== 'POST' :

        payable=request.form['payable']
        pending=request.form['pending']
        payed=request.form['payed']
        date=request.form['date']
        username=request.form['username']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO userd VALUES (NULL, % s, % s, % s, % s, % s)', (username,date,payable,payed,pending))
        mysql.connection.commit()
        msg = 'Purchase registered !'

    return render_template('newpurchase.html',msg=msg)

@app.route('/userlist')
def user_list():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT username,email FROM user')
    data = cursor.fetchall()
    colnames=['USERNAME!','EMAIL-ID!']
    print(data)





    return render_template('userlist.html',data=data,colnames=colnames)


@app.route('/cplist')
def cplist():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT date,username,complaint FROM complaint')
    data = cursor.fetchall()
    colnames=['DATE !','USERNAME!','COMPLAINT !']

    return render_template('complaintlist.html',colnames=colnames,data=data)

@app.route('/notification')
def notif():

    username =  session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT date,notification FROM notification WHERE username=% s',(username,))
    data = cursor.fetchall()
    colnames=['DATE!    ','NOTIFICATION!    ']

    return render_template('notification.html',colnames=colnames,data=data)

@app.route('/newpay',methods=['GET','POST'])
def newpay():
    msg=''
    if request.method== 'POST' :


        notification=request.form['notification']
        date=request.form['date']
        username=request.form['username']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO notification VALUES (NULL, % s, % s, % s)', (username,date,notification))
        mysql.connection.commit()
        msg = 'Payment notification send !'
    return render_template('newpay.html',msg=msg)

@app.route('/sendnot')
def sendnot():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT date,username,notification FROM notification')
    data = cursor.fetchall()
    colnames=['DATE !','USERNAME!','NOTIFICATIONS !']

    return render_template('sendnot.html',data=data,colnames=colnames)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port = 8080)