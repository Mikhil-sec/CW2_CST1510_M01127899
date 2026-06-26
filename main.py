from app_model.db import get_connection
from app_model.schema import create_user_table
from app_model.users import New_User, register_user,login_User
from app_model.cyber_incidents import migrate_cyber_incidents
from app_model.it_tickets import migrate_it_tickets
from app_model.metadatas import migrate_metadatas

def Migrate_All_Tables():
    conn = get_connection()
    migrate_cyber_incidents(conn)
    migrate_it_tickets(conn)
    migrate_metadatas(conn)
def cli_authentication_system():
    while True:
        print('1. To Register\n2. To Log in\n3. To Exit')
        choice = input(': > ')
        if choice == '1':
            register_user()
        elif choice == '2':
            if login_User() == True :
                print("Login successful!")
            else:
                print("Incorrect login")
        elif choice == '3':
            print('Goodbye!'); 
            break


def main():

    print("Welcome")
    cli_authentication_system()

if __name__ == "__main__":
    main()
    