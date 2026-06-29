import pandas as pd
#Comments!
def migrate_metadatas(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadatas' ")
    results = cur.fetchone()
    if results is None:
        data = pd.read_csv(r'DATA\datasets_metadata.csv')
        data.to_sql('metadatas', conn, index=False)
    else:
        #table already exist
        pass

def get_all_metadatas(conn):
    sql = 'SELECT * FROM metadatas'
    return pd.read_sql(sql, conn)