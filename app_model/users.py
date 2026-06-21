import bcrypt

def New_User():
    Username = input("Hello, Please enter your username")
    Password = input("Please enter your password")
    #add a check if username unique and password strong and verification of password
    
    #



def Login():
    Username = input("Hello, Please enter your username")
    Password = input("Please enter your password")
    #add a check login

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



def main():
    print("Main is here")

