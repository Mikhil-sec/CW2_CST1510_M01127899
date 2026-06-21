import pandas as pd

def migrate_metadatas(conn):
    data = pd.read_csv('CW2_CST1510_M01127899\DATA\datasets_metadata.csv')
    data.to_sql('metadatas', conn)

def get_all_metadatas(conn):
    sql = 'SELECT * FROM metadatas'
    return pd.read_sql(sql, conn)