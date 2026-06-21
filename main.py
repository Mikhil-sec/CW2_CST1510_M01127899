from app_model.db import get_connection
from app_model.schema import create_user_table
from app_model.users import New_User
from app_model.cyber_incidents import migrate_cyber_incidents
def main():

    print("Welcome")
    conn = get_connection()
    create_user_table(conn)
    New_User()
    #testing cyber incidents migration:
    migrate_cyber_incidents(conn)

if __name__ == "__main__":
    main()
    