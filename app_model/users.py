import bcrypt
from app_model.schema import add_user, get_user, add_user_with_role, log_login, get_user_role
from app_model.db import get_connection
import sqlite3 #Imported to use its error handling syntax in Register User function
import re
import os
from dotenv import load_dotenv
from pathlib import Path
#getting global connection to database
conn = get_connection()

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

#==========================================
#    SECURE PASSWORD STORAGE(HASHING)
#==========================================

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

#Taking admin code from env
env_path = Path(__file__).parent.parent / ".env"  # Define the path to the .env file
load_dotenv(env_path)  # Load environment variables from the .env

ADMIN_CODE = os.getenv("ADMIN_CODE", "CortexAdmin2026!")  # retrieve admin code from .env or use default value if not found

def Register_User_Streamlit(Username:str,Password:str, Admin_Code=""): #type hint so strip() gets recognized
    #Takes username/password as arguments instead of asking via input()
    
    if Username.strip() == "": #using strip to remove whitespace
        return False, "Username cannot be empty"
    
    if Password.strip() == "":
        return False, "Password cannot be empty"
    #Determine role based on admin code
    role = 'admin' if Admin_Code.strip() == ADMIN_CODE else 'user'


    existing_user = get_user(conn, Username)
    if existing_user is not None:
        return False, "Username already exists." #returns both boolean and string

    Hash_Psw = HashPassword_Generator(Password)
    try:
        add_user_with_role(conn, Username, Hash_Psw, role)
        return True, f"Account successfully registered! Role: {role.capitalize}" #returns both boolean and string
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        print(f"Registering user to database error: {e}") #prints to terminal for developer/debugger
        return False, "An unexpected error occurred. Please try again."
def check_password_strength(password):
    #Returns (strength_label, score_out_of_5, list_of_missing_requirements)
    #score: 0-2 = Weak, 3 = Medium, 4-5 = Strong
    missing = []
    score = 0
    if len(password) < 8:
        missing.append("At least 8 characters")
        return "Weak", 0, missing  # return immediately, no point checking anything else
    score +=1
    if re.search(r"[A-Z]",password):
        score +=1
    else:
        missing.append("At least one uppercase letter")
    if re.search(r"[a-z]",password):
        score +=1
    else:
        missing.append("At least one lowercase letter")
    if re.search(r"[0-9]",password):
        score += 1
    else:
        missing.append("At least one number")
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        score += 1
    else:
        missing.append("At least one special character (!@#$% etc.)")
    if score <= 2:
        label = "Weak"
    elif score <= 3:
        label = "Medium"
    else:
        label = "Strong"

    return label, score, missing   

def Login_User_Streamlit(Username,Password):
    #Streamlit function for Login
    #check for empty input
    if Username.strip() == "":
        return False, "Username cannot be empty", None
    if Password.strip() == "":
        return False, "Password cannot be empty", None
    try:
        #check if username exist
        user = get_user(conn, Username)
        if user is None:
            return False, "Username does not exist", None
        #takes the hash in database
        stored_Hash = user[2]
        #checks the passwords if hash matches
        is_valid = Password_Checker(Password, stored_Hash)
        if is_valid:
            #logs time of login
            log_login(conn, Username)
            role = get_user_role(conn, Username)
            return True, "Login successful!", role
        else:
            return False, "Incorrect Password", None
    except Exception as e: #general error handling
        print(f"Login error: {e}")
        return False, "Login failed due to a system error.", None
    


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