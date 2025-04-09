import pymysql
import pymysql.cursors
import creds

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
    FROM movie LIMIT 100;"""
  return execute_query(query)
