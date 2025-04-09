from flask import Flask
from flask import render_template, request
import pymysql
import creds
from dbCode import *

app = Flask(__name__)

@app.route('/')
def index():
    #get items list from the database
    movies = get_movies()
    return render_template('index.html', items=movies)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= '5000', debug=True)