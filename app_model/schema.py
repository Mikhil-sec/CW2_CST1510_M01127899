
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
    sql = 'INSERT INTO users (username, password_hash) VALUES (?,?);'
    cur.execute(sql, (name, hash_Psw))
    conn.commit()