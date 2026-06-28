import bcrypt
from app_model.schema import add_user, get_user
from app_model.db import get_connection

#CLI based user input
def New_User():
    Username = input("Hello, Please enter your username: ")
    Password = input("Please enter your password: ")
    #add a check if username unique and password strong and verification of password
    Hash_Psw = HashPassword_Generator(Password)
    conn = get_connection()
    add_user(conn,Username,Hash_Psw)

    #try catch



def Login():
    Username = input("Hello, Please enter your username")
    Password = input("Please enter your password")
    #add a check login -- old code for CLI - does it need to exist and work properly?

def Password_Checker(Inputted_Psw,Hash_Psw):
    Byte_Hash_Psw = Hash_Psw.encode('utf-8')
    Byte_Inputted_Psw = Inputted_Psw.encode('utf-8')
    Is_Valid = bcrypt.checkpw(Byte_Inputted_Psw,Byte_Hash_Psw)
    return Is_Valid

def HashPassword_Generator(psw):
    byte_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')

#=======================================
#    STREAMLIT REGISTRATION & LOGIN
#=======================================


def Register_User_Streamlit(Username,Password):
    """Takes username/password as arguments instead of asking via input()."""
    conn = get_connection()

    existing_user = get_user(conn, Username)
    if existing_user is not None:
        return False, "Username already exists." #returns both boolean and string

    Hash_Psw = HashPassword_Generator(Password)
    add_user(conn, Username, Hash_Psw)
    return True, "User successfully registered!" #returns both boolean and string

def Login_User_Streamlit(Username,Password):
    """Streamlit function for Login"""
    
    conn = get_connection()
    user = get_user(conn, Username)
    
    if user is None:
        
        return False, "Username does not exist"
    stored_Hash = user[2]
    
    is_valid = Password_Checker(Password,stored_Hash)
    
    if is_valid == True:
        
        return True, "Login successful!"
    else:
        return False, "Incorrect Password"
    


#=====================================
#    FLAT FILE REGISTRATION & LOGIN
#=====================================

def register_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    hash_password = HashPassword_Generator(password)
    with open(r'DATA\users.txt', 'a') as f:
        f.write(f'{name},{hash_password}\n')
    print('User successfully registered!')

def login_User():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    with open(r'DATA\users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(',')
        if name == user_name and Password_Checker(password,user_hash):
            return True
    return False