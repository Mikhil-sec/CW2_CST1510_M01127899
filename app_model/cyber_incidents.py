import pandas as pd

def migrate_cyber_incidents(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cyber_incidents'")
    results = cur.fetchone()
    if results is None:
        data = pd.read_csv(r'DATA\cyber_incidents.csv')
        data.to_sql('cyber_incidents', conn,index=False)
    else:
        #table already exist
        pass

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    return pd.read_sql(sql, conn)