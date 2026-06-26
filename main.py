from app_model.db import get_connection
from app_model.schema import create_user_table
from app_model.users import New_User, register_user,login_User, Register_User_Streamlit, Login_User_Streamlit
from app_model.cyber_incidents import migrate_cyber_incidents
from app_model.it_tickets import migrate_it_tickets
from app_model.metadatas import migrate_metadatas

import streamlit as st

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

#========================
# STREAMLIT FUNCTIONS
#========================

def Initialise_Session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None

def Dashboard_Login_Register():
    st.title("Cortex")
    st.caption("Multi-domain intelligence platform")

    menu = st.sidebar.selectbox("Menu",["Login","Register"])
    if menu == "Register":
        st.subheader("Create New Account")
        username = st.text_input("Username",key="register_username")  #keys used to identify each input box, especially since 2 username used
        password = st.text_input("Password", type="password",key="register_password") #type = "password" to hide password input on screen
        if st.button("Register"):
            success, message = Register_User_Streamlit(username,password)
            if success:
                st.session_state["logged_in"]= True
                st.session_state["username"] = username
                st.success(message)
                st.rerun()

            else:
                st.error(message)
    elif menu == "Login":
        st.subheader("Login to your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password",type="password",key="login_password")
        if st.button("Login"):
            success, message = Login_User_Streamlit(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def User_Dashboard():
    st.title(f"Welcome, {st.session_state["username"]} !")
    st.write("This is the dashboard beep bop 😎")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.rerun()

def Streamlit_main():
    if st.session_state["logged_in"]:
        User_Dashboard()
    else:
        Dashboard_Login_Register()

def main():
    Initialise_Session()
    Streamlit_main()
    
if __name__ == "__main__":
    main()
    