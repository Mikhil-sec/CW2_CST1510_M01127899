import pandas as pd
#comments!
def migrate_it_tickets(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='it_tickets'")
    results = cur.fetchone()
    if results is None:
        data = pd.read_csv(r'DATA\it_tickets.csv')
        data.to_sql('it_tickets', conn, index=False)
    else:
        #table already exist
        pass

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    return pd.read_sql(sql, conn)