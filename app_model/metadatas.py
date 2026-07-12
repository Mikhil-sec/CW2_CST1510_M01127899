import pandas as pd
from pathlib import Path
def migrate_metadatas(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadatas' ")
    results = cur.fetchone()
    if results is None:
        metadatas_path = Path(__file__).parent.parent / "DATA" / "datasets_metadata.csv"
        data = pd.read_csv(metadatas_path)
        data.to_sql('metadatas', conn, index=False)

def get_all_metadatas(conn):
    sql = 'SELECT * FROM metadatas'
    return pd.read_sql(sql, conn)