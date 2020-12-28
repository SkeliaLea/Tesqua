from flask import Flask, render_template, json, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask import flash
import MySQLdb.cursors

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user_db'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password,))
        login = cursor.fetchone()
        if login:
            session['loggedin'] = True
            session['id'] = login['id']
            session['username'] = login['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Logged in Failed!'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
    
"""@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response"""


if __name__ == '__main__':
    app.debug = True
    app.run()