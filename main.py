from app_model.db import get_connection
from app_model.schema import create_user_table
from app_model.users import New_User, register_user,login_User, Register_User_Streamlit, Login_User_Streamlit
from app_model.cyber_incidents import migrate_cyber_incidents, get_all_cyber_incidents
from app_model.it_tickets import migrate_it_tickets, get_all_it_tickets
from app_model.metadatas import migrate_metadatas, get_all_metadatas
from app_model.ai_assistant import ask_ai_about_data

import streamlit as st
import pandas as pd
# NEED COMMENTSSS
def Migrate_All_Tables():
    conn = get_connection()
    create_user_table(conn)
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
    conn = get_connection()
    st.title(f"Welcome, {st.session_state["username"]} !")
    st.write("Dashboard beep boop 😎")
    if st.button("Logout"): #reseting states
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["cyber_chat"]=[]
        st.session_state["ITtickets_chat"]= []
        st.session_state["metadata_chat"]=[]
        st.rerun() #force rerun to go back to login page
    st.divider()
    #selecting which dataset's dashboard to display
    dataset_choice = st.sidebar.selectbox("Choose a dataset",["Cyber incidents", "IT Tickets", "Dataset Metadata"])


    if dataset_choice == "Cyber incidents":
        df = get_all_cyber_incidents(conn)
        st.subheader("Cyber incidents")
        st.dataframe(df)
        col1, col2 = st.columns(2)
        with col1: #use of with to specify which code in which container for cleaner look
            st.caption("By Severity")
            st.bar_chart(df["severity"].value_counts()) #change bar chart for plotly interface later !!
        with col2:
            st.caption("By Category")
            st.bar_chart(df["category"].value_counts())
        Streamlit_render_ai_chat(df,"Cyber Incidents",chat_key="cyber_chat")


    elif dataset_choice == "IT Tickets":
        df=get_all_it_tickets(conn)
        st.subheader("IT Tickets")
        st.dataframe(df)
        col1, col2 = st.columns(2)
        with col1:
            st.caption("By Priority")
            st.bar_chart(df["priority"].value_counts())
        with col2:
            st.caption("By Status")
            st.bar_chart(df["status"].value_counts())
        

        st.caption("Average Resolution Time by Priority (hours)")
        st.bar_chart(df.groupby("priority")["resolution_time_hours"].mean())

        Streamlit_render_ai_chat(df,"IT Tickets",chat_key="ITtickets_chat")

    elif dataset_choice == "Dataset Metadata":
        #ADD MORE TO THIS DASHBOARD
        df = get_all_metadatas(conn)
        st.subheader("Dataset Metadata")
        st.dataframe(df)

        Streamlit_render_ai_chat(df,"Dataset Metadata",chat_key="metadata_chat")

def Streamlit_main():
    if st.session_state["logged_in"]:
        User_Dashboard()
    else:
        Dashboard_Login_Register()

def Streamlit_render_ai_chat(df,dataset_name, chat_key):
    st.divider()
    st.subheader(f"💬 Ask about {dataset_name}")
    if chat_key not in st.session_state:
        st.session_state[chat_key]=[]
    for role, text in st.session_state[chat_key]:
        with st.chat_message(role):
            st.write(text)

    user_question = st.chat_input(f"Ask a question about {dataset_name}...",key=f"{chat_key}_input")
    if user_question:
        st.session_state[chat_key].append(("user",user_question))
        with st.spinner("Thinking..."):
            answer = ask_ai_about_data(user_question,df,dataset_name)
        
        st.session_state[chat_key].append(("assistant",answer))
        st.rerun()
        

def main():
    Migrate_All_Tables()
    Initialise_Session()
    Streamlit_main()
    
if __name__ == "__main__":
    main()
    