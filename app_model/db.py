import sqlite3

def get_connection():
    """Opens and returns a connection to the SQLite database."""
    conn = sqlite3.connect('CW2_CST1510_M01127899\DATA\project_data.db')
    return conn
