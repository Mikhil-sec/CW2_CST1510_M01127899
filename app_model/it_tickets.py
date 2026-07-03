import pandas as pd
from pathlib import Path
def migrate_it_tickets(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='it_tickets'")
    results = cur.fetchone()
    if results is None:
        ticket_path = Path(__file__).parent.parent / "DATA" / "it_tickets.csv"
        data = pd.read_csv(ticket_path)
        data.to_sql('it_tickets', conn, index=False)
    
def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    return pd.read_sql(sql, conn)