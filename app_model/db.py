import sqlite3
#Function to get a connection to the SQLite database
def get_connection():
    """Opens and returns a connection to the SQLite database."""
    conn = sqlite3.connect(r'DATA\project_data.db')
    return conn
