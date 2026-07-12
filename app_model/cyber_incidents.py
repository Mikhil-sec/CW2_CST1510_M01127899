import pandas as pd
from pathlib import Path #using pathlib so that the code works on any operating system(Windows/Mac/Linux).
#used to migrate the cyber_incidents table from the csv file to the database:
def migrate_cyber_incidents(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cyber_incidents'")
        results = cur.fetchone()
        if results is None:
            cyber_path = Path(__file__).parent.parent / "DATA" / "cyber_incidents.csv"
            data = pd.read_csv(cyber_path)
            data.to_sql('cyber_incidents', conn,index=False)
    except Exception as e:
        print(f"Error migrating cyber_incidents table: {e}") #Proper error for debugging purpose on terminal output
        
        
#used to get all the cyber incidents from the database:
def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    return pd.read_sql(sql, conn)