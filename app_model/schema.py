import pandas as pd
import datetime
def create_user_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user' )
        ;'''
    cur.execute(sql)
    conn.commit()
def create_user_login_activity_table(conn):
    cur =conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS login_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        login_timestamp TEXT NOT NULL
        );'''
    cur.execute(sql)
    conn.commit()

def log_login(conn, username):
    #Records a login event with current timestamp.
    cur = conn.cursor()
    timestamp = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    cur.execute(
        'INSERT INTO login_activity (username, login_timestamp) VALUES (?, ?)',
        (username, timestamp)
    )
    conn.commit()

def users_info_display(conn):
    #Returns all users as a DataFrame — no password hashes
    sql = 'SELECT id, username, role FROM users'
    return pd.read_sql(sql, conn)

def get_login_activity(conn):
    #Returns full login activity log as a DataFrame
    sql = '''SELECT username, login_timestamp 
             FROM login_activity 
             ORDER BY login_timestamp DESC'''
    return pd.read_sql(sql, conn)

def update_user_role(conn, username, new_role):
    #Promotes or demotes a user's role
    cur = conn.cursor()
    cur.execute(
        'UPDATE users SET role = ? WHERE username = ?',
        (new_role, username)
    )
    conn.commit()

def get_user_role(conn, username):
    #Returns just the role string for a given username
    cur = conn.cursor()
    cur.execute('SELECT role FROM users WHERE username = ?', (username,))
    result = cur.fetchone()
    return result[0] if result else 'user'

def add_user_with_role(conn, username, password_hash, role='user'):
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
        (username, password_hash, role)
    )
    conn.commit()

def add_user(conn, name, hash_Psw):
    cur = conn.cursor()
    sql = 'INSERT INTO users (username, password_hash) VALUES (?,?)'
    cur.execute(sql, (name, hash_Psw))
    conn.commit()

def get_all_users(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

def get_user(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?',(name,))
    return cur.fetchone()

def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = ? WHERE username =?', (new_name, old_name))
    conn.commit()

def delete_user(conn, user_name):
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE username = ?',(user_name,))
    conn.commit()