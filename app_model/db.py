import sqlite3
from pathlib import Path #using pathlib so that the code works on any operating system(Windows/Mac/Linux).

#Function to get a connection to the SQLite database
def get_connection():
    """Opens and returns a connection to the SQLite database."""
    db_path = Path(__file__).parent.parent / "DATA" / "project_data.db"  # Define the path to the database file
    conn = sqlite3.connect(db_path, check_same_thread=False)  # Establish a connection to the database
    return conn
