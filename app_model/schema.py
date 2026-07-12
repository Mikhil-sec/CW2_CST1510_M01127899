
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