from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
import pymysql
import creds
from dbCode import *
from functools import wraps

app = Flask(__name__)

app.secret_key = '7de80d625bbc10877eb0a36ec93196e36a55ed40259588a3'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user already exists
        if get_user(username):
            return "Username already exists. Try another one."

        # Create user in DynamoDB
        create_user(name, username, password)

        # Redirect to login page (which is your '/')
        return redirect(url_for('login'))

    # If someone hits /signup via GET, show the signup form
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists and password is correct
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
            
    # If someone hits /login via GET, show the login form
    return render_template('login.html')

@app.route('/index')
@login_required
def index():
  if 'user' not in session:
        return redirect(url_for('login'))
  
  #get items list from the database
  movies = get_movies()
  return render_template('index.html', items=movies)

@app.route('/logout')
def logout():
    # Clear the session (this logs the user out)
    session.pop('user', None)
    # Redirect to the login page
    return redirect(url_for('login'))

"""@app.route('/')
def login():
    return render_template('signup.html')

@app.route('/home')
def index():
    #get items list from the database
    movies = get_movies()
    return render_template('index.html', items=movies)"""

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= '5000', debug=True)