from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
import pymysql
import creds
import json
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

@app.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    raw_selected = request.form.get('selected_movies')
    if not raw_selected:
        flash("No movies selected.", "danger")
        return redirect(url_for('index'))

    selected_titles = json.loads(raw_selected)
    username = session['user']
    movies = get_movies()

    # Map titles to IDs
    title_to_id = {m['title']: m['movie_id'] for m in movies}
    added = []

    for title in selected_titles:
        movie_id = title_to_id.get(title)
        if movie_id:
            add_movie_to_watchlist(username, movie_id)
            added.append(title)

    if added:
        flash(f"Added {', '.join(added)} to your watchlist.", "success")
    else:
        flash("No valid movies were added.", "danger")

    return redirect(url_for('index'))

@app.route('/watchlist')
@login_required
def watchlist():
    username = session['user']
    
    # Get user's saved movie IDs from DynamoDB
    user = get_user(username)
    movie_ids = user.get('watchlist', [])  # default to empty list

    # If watchlist is empty
    if not movie_ids:
        return render_template('watchlist.html', movies=[])

    # Fetch movie details from SQL
    placeholders = ','.join(['%s'] * len(movie_ids))
    query = f"""SELECT movie_id, title, overview FROM movie WHERE movie_id IN ({placeholders})"""
    movies = execute_query(query, movie_ids)

    return render_template('watchlist.html', movies=movies)

@app.route('/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist():
    username = session['user']
    movie_id = request.form.get('movie_id')

    if not movie_id:
        return redirect(url_for('watchlist'))
    
    movie_id = int(movie_id)

    # Fetch current watchlist
    user = get_user(username)
    watchlist = user.get('watchlist', [])

    # Remove movie_id if it's in the list
    if movie_id in watchlist:
        watchlist.remove(movie_id)
        # Update DynamoDB
        user_table.update_item(
            Key={'username': username},
            UpdateExpression='SET watchlist = :w',
            ExpressionAttributeValues={':w': watchlist}
        )

    return redirect(url_for('watchlist'))


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