from app_model.db import get_connection
from app_model.schema import create_user_table
from app_model.users import New_User
from app_model.cyber_incidents import migrate_cyber_incidents
from app_model.it_tickets import migrate_it_tickets
from app_model.metadatas import migrate_metadatas

def Migrate_All_Tables():
    conn = get_connection()
    migrate_cyber_incidents(conn)
    migrate_it_tickets(conn)
    migrate_metadatas(conn)


def main():

    print("Welcome")
    conn = get_connection()
    create_user_table(conn)
    New_User()
    Migrate_All_Tables()
    #testing cyber incidents migration:
    #migrate_cyber_incidents(conn)

if __name__ == "__main__":
    main()
    