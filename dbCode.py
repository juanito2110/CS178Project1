import pymysql
import pymysql.cursors
import creds
import boto3
import bcrypt

def get_conn():
  conn = pymysql.connect(
    host = creds.host,
    user = creds.user,
    password = creds.password,
    db = creds.db,
    cursorclass=pymysql.cursors.DictCursor
  )
  return conn

def execute_query(query, args=()):
  conn = get_conn()
  try:
    with conn.cursor() as cur:
      cur.execute(query, args)
      rows = cur.fetchall()
    return rows
  finally:
    conn.close()

def get_movies():
  query = """SELECT movie_id,
    ROW_NUMBER() OVER (ORDER BY title) AS number,
    title, overview
    FROM movie;"""
  return execute_query(query)

def add_movie_to_watchlist(username, movie_id):
    # Use add if the field exists, or set if it doesn’t
    user = get_user(username)
    watchlist = user.get('watchlist', [])
    
    if movie_id not in watchlist:
        watchlist.append(movie_id)
        user_table.update_item(
            Key={'username': username},
            UpdateExpression='SET watchlist = :wl',
            ExpressionAttributeValues={':wl': watchlist}
        )


#Create DynamoDB session and reference the users table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
user_table = dynamodb.Table('users')

def create_user(name, username, password):
  hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
  user_table.put_item(Item={
    'name': name,
    'username': username,
    'password': hashed_pw,
  })

def get_user(username):
  response = user_table.get_item(Key={'username': username})
  return response.get('Item')

def update_user_profile(username, name, favouriteGenre):
  user_table.update_item(
    Key={'username': username},
    UpdateExpression='SET name = :fn, favouriteGenre = :fGenre',
    ExpressionAttributeValues={
      ':fn': name,
      ':fGenre': favouriteGenre
    }
  )

def check_password(username, password):
  user = get_user(username)
  if not user:
    return False
  return bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))