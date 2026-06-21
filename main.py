from app_model.db import get_connection
from app_model.schema import create_user_table

def main():

    print("Welcome")
    conn = get_connection()
    create_user_table(conn)

if __name__ == "__main__":
    main()
    