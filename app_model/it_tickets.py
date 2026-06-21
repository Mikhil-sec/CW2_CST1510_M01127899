import pandas as pd

def migrate_it_tickets(conn):
    data = pd.read_csv('CW2_CST1510_M01127899\DATA\it_tickets.csv')
    data.to_sql('it_tickets', conn)

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    return pd.read_sql(sql, conn)