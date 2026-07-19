#importing all necessary functions from other files
from app_model.db import get_connection
from app_model.schema import create_user_table , delete_user, create_user_login_activity_table, get_user_role, users_info_display, get_login_activity, update_user_role
from app_model.users import register_user,login_User, Register_User_Streamlit, Login_User_Streamlit, check_password_strength
from app_model.cyber_incidents import migrate_cyber_incidents, get_all_cyber_incidents
from app_model.it_tickets import migrate_it_tickets, get_all_it_tickets
from app_model.metadatas import migrate_metadatas, get_all_metadatas
from app_model.ai_assistant import ask_ai_about_data, suggest_strong_passwords, cross_dataset_analysis
#importing necessary library
import streamlit as st
import plotly.express as px

#global variable to hold the database connection
conn = get_connection() 

#Page configuration
st.set_page_config("Cortex","🛡️","wide")

#function to migrate all tables in the database
def Migrate_All_Tables():
    
    create_user_table(conn)
    create_user_login_activity_table(conn)
    migrate_cyber_incidents(conn)
    migrate_it_tickets(conn)
    migrate_metadatas(conn)
#====================================
# Old CLI from initial project steps
#====================================
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

#function to initialise session state variables for login status, username and role
def Initialise_Session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None
#function to render the login and register dashboard
def Dashboard_Login_Register():
    col1,col2,col3 = st.columns([1,2,1]) #puts dashboard in center
    with col2:
        st.title("🛡️ Cortex")
        st.caption("Multi-domain intelligence platform")
        st.divider()
        menu = st.selectbox("Menu",["Login","Register"],label_visibility="collapsed")
        if menu == "Register":
            st.subheader("Create New Account")
            username = st.text_input("Username",key="register_username")  #keys used to identify each input box, especially since 2 username used (register & login)
            password = st.text_input("Password", type="password",key="register_password") #type = "password" to hide password input on screen
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            #Collapsible admin code field
            with st.expander("🔐 Have an admin code?"):
                admin_code = st.text_input("Admin Code", type="password", key="admin_code")

            # default before user types anything
            strength_label = "Weak"
            score = 0
            missing = []
            success = False
            message = ""
            # Live password strength display
            if password:
                strength_label,score,missing = check_password_strength(password)
                # Color and progress value
                if strength_label == "Weak":
                    bar_color = "🔴"
                    progress_val = score/5
                elif strength_label == "Medium":
                    bar_color = "🟡"
                    progress_val = score / 5
                else:
                    bar_color = "🟢"
                    progress_val = 1.0

                st.progress(progress_val)
                st.caption(f"{bar_color} Password strength: **{strength_label}**")
            #Display of missing requirements
            if missing:
                with st.expander("What's missing?"):
                    for req in missing:
                        st.caption(f"• {req}")
            #AI password suggestion button - only if not strong pw label
            if strength_label != "Strong":
                if st.button("💡 Suggest stronger passwords"):
                    with st.spinner("Generating suggestions..."):
                        suggestions = suggest_strong_passwords(password)
                    st.info(suggestions)

            #Register button logic
            if st.button("Register",width="stretch"):
                if not password:
                    st.error("Password cannot be empty.")
                elif strength_label == "Weak":
                    st.error("Password is too weak to register. Please strengthen it first.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message= Register_User_Streamlit(username,password, admin_code)
                if success:
                    st.session_state["logged_in"]= True
                    st.session_state["username"] = username
                    role = get_user_role(conn, username)
                    st.session_state["role"] = role
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)
        elif menu == "Login":
            st.subheader("Login to your Account")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password",type="password",key="login_password")
            if st.button("Login",width="stretch"):
                success, message, role = Login_User_Streamlit(username, password)
                if success:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = role
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

def User_Dashboard():
    #creating and using a Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state["username"]}")
        role = st.session_state["role"]
        if role == 'admin':
            st.caption("🔴 Administrator")
        else:
            st.caption("🟢 User")
        st.divider()
        # Showing admin panel option only for admins
        if role == 'admin':
            view = st.selectbox("🖥️ View", ["Dashboard", "Admin Panel"])
        else:
            view = "Dashboard"

        if view == "Dashboard":
            #selecting which dataset's dashboard to display
            dataset_choice = st.selectbox(
                "📂 Choose a dataset",
                ["Cyber Incidents", "IT Tickets", "Dataset Metadata","🧠 Intelligence"]
            )
        st.divider()
        #Log out button
        if st.button("🚪 :red[**Log out**]",width="stretch"): #reseting states
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["role"] = None
            st.session_state["cyber_chat"]=[]
            st.session_state["ITtickets_chat"]= []
            st.session_state["metadata_chat"]=[]
            st.rerun() #force rerun to go back to login page
        #Each dashboard call option
        
        #Delete account button
        @st.dialog("Delete Account")
        def confirm_delete():
            st.warning("This action cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes"):
                    conn = get_connection()
                    delete_user(conn, st.session_state["username"])
                    st.session_state["logged_in"] = False
                    st.session_state["username"] = None
                    st.session_state["role"] = None
                    st.session_state["cyber_chat"]=[]
                    st.session_state["ITtickets_chat"]= []
                    st.session_state["metadata_chat"]=[]
                    st.success("Account deleted successfully.")
                    conn.close()
                    st.rerun()
            with col2:
                if st.button("No"):
                    st.rerun()
        if st.button("🗑️ :red[Delete Account]",width="stretch"):
            confirm_delete()
    if role == 'admin' and view == "Admin Panel":
            Render_Admin_Panel(conn)
    elif view == "Dashboard":
        if dataset_choice == "Cyber Incidents":
            Render_Cyber_Incidents()
        elif dataset_choice == "IT Tickets":
            Render_IT_Tickets()
        elif dataset_choice == "Dataset Metadata":
            Render_Metadata()
        elif dataset_choice == "🧠 Intelligence":
            Render_Intelligence()

#Admin Panel Dashboard
def Render_Admin_Panel(conn):
    st.title("🔐 Admin Panel")
    st.caption("Restricted access — administrators only")
    st.divider()
    # User management section
    st.subheader("👥 Registered Users")
    users_df = users_info_display(conn)
    st.dataframe(users_df)
    st.divider()

    # Role management
    st.subheader("⚙️ Role Management")
    col1, col2, col3 = st.columns(3)

    with col1:
        target_user = st.selectbox("Select User",users_df["username"].tolist())
    with col2:
        new_role = st.selectbox("Assign Role",["user", "admin"])
    with col3:
        st.write("")
        st.write("")
        if st.button("Update Role", width="stretch"):
            if target_user == st.session_state["username"]:
                st.error("You cannot change your own role.")
            else:
                update_user_role(conn, target_user, new_role)
                st.success(f"{target_user} is now a {new_role}.")
                st.rerun()

    st.divider()

    # Delete user
    st.subheader("🗑️ Delete User")
    col1, col2 = st.columns(2)
    with col1:
        user_to_delete = st.selectbox("Select User to Delete",users_df["username"].tolist(),key="delete_user_select")
    with col2:
        st.write("")
        st.write("")
        if st.button("🗑️ Delete User", width="stretch"):
            if user_to_delete == st.session_state["username"]:
                st.error("You cannot delete your own account.")
            else:
                delete_user(conn, user_to_delete)
                st.success(f"User '{user_to_delete}' deleted.")
                st.rerun()

    st.divider()

    # Login activity log
    st.subheader("📋 Login Activity Log")
    activity_df = get_login_activity(conn)

    if activity_df.empty:
        st.info("No login activity recorded yet.")
    else:
        # Metric
        total_logins = len(activity_df)
        unique_users = activity_df["username"].nunique()
        col1, col2 = st.columns(2)
        col1.metric("Total Login Events", total_logins)
        col2.metric("Unique Users", unique_users)

        st.dataframe(activity_df)

        # Chart — logins per user
        login_counts = activity_df["username"].value_counts().reset_index()
        login_counts.columns = ["username", "logins"]
        fig = px.bar(
            login_counts,
            x="username",
            y="logins",
            title="Login Frequency by User",
            color_discrete_sequence=["#00d4ff"]
        )
        fig.update_yaxes(dtick=1)
        st.plotly_chart(fig)

#Cyber Incidents Dashboard
def Render_Cyber_Incidents():
    st.title("🔴 Cyber Incidents")
    df = get_all_cyber_incidents(conn)
    # Metric cards Data
    total = len(df)
    critical = len(df[df["severity"] == "Critical"])
    open_incidents = len(df[df["status"] == "Open"])
    # Metric cards display
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Incidents",total)
    col2.metric("Critical", critical, delta=f"{critical} need attention", delta_color="inverse")
    col3.metric("Open",open_incidents,delta=f"{open_incidents} unresolved",delta_color="inverse")
    st.divider()

    # AI Risk Summary button
    if st.button("🧠 Generate AI Risk Summary"):
        with st.spinner("Analysing threat landscape..."):
            try:
                summary = ask_ai_about_data("Give a concise executive risk summary of this dataset."
                                            "Highlight the most critical threats, patterns, and immediate recommended actions."
                                            "Format as a brief SOC analyst briefing.",
                                            df,
                                            "Cyber Incidents")
                st.info(summary)
            except Exception as e:
                #Error output for user
                st.error("Risk summary unavailable. Please try again.")
                #Error output for developer/debugger on terminal
                print(f"Risk summary error: {e}")
    st.divider()
    # Filters
    col1,col2 = st.columns(2)
    with col1:
        severity_options = ["All"] + sorted(df["severity"].unique().tolist()) #turning to list and sorting to make it easier for user to select
        severity_filter = st.selectbox("Filter by Severity",severity_options)
    with col2:
        status_options = ["All"] + sorted(df["status"].unique().tolist())
        status_filter = st.selectbox("Filter by Status",status_options)
    # Applying filters
    filtered_df = df.copy()
    if severity_filter != "All":
        filtered_df = filtered_df[filtered_df["severity"] == severity_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]
    
    st.subheader(f"Incidents ({len(filtered_df)} shown)")
    st.dataframe(filtered_df,width="stretch")

    #CSV export
    csv = filtered_df.to_csv(index=False)
    st.download_button("⬇️ Export filtered data as CSV",csv,"cyber_incidents_filtered.csv","text/csv")
    st.divider()

    #Plotly charts
    col1,col2 = st.columns(2)
    #manually assigning each severity category a color
    severity_colors = {
        "Critical": "#ef4444",
        "High": "#f97316",
        "Medium": "#eab308",
        "Low":"#22c55e"
    }
    with col1:
        #create dataframe with only the severity categories and the counts of each of them
        severity_counts = df["severity"].value_counts().reset_index()
        severity_counts.columns = ["severity","count"] #manually naming the columns headers
        #using plotly express bar chart
        fig = px.bar(
            severity_counts, #Dataframe to plot
            "severity", #label for x axis
            "count", #label for y axis
            "severity", #tells plotly to color each bar differently based on the severity column value
            color_discrete_map=severity_colors, #Passing the color dictionary to the specific color to each severiy level
            title="Incidents by Severity"
        )
        #layout customisation
        fig.update_layout(
            font_color = "#e2e8f0",
            showlegend=False #turns off redundant color keys
        )
        st.plotly_chart(fig)
    #same as col1 but with category as key parameter
    with col2:
        category_counts = df["category"].value_counts().reset_index()
        category_counts.columns = ["category","count"]
        fig2=px.bar(
            category_counts,
            "count",
            "category",
            orientation="h", #makes bars horizontal
            title="Incidents by Category",
            color_discrete_sequence=["#00d4ff"]
        )
        fig2.update_layout(
            font_color="#e2e8f0"
        )
        st.plotly_chart(fig2)
    Streamlit_render_ai_chat(df,"Cyber Incidents","cyber_chat")
#IT ticket dashboard
def Render_IT_Tickets():
    st.title("🎫 IT Tickets")
    df = get_all_it_tickets(conn) #putting the dataframe created from database in df
    #Metric cards data
    total = len(df)
    high_priority = len(df[df["priority"] == "High"])
    avg_resolution = round(df["resolution_time_hours"].mean(),1)

    #Metric cards display
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Tickets", total)
    col2.metric("High Priority",high_priority,delta=f"{high_priority} flagged",delta_color="inverse")
    col3.metric("Avg Resolution Time",f"{avg_resolution}h")
    st.divider()
    # Filters
    col1,col2 = st.columns(2)
    with col1:
        priority_options = ["All"] + sorted(df["priority"].unique().tolist())
        priority_filter = st.selectbox("Filter by Priority", priority_options)
    with col2:
        status_options = ["All"] + sorted(df["status"].unique().tolist())
        status_filter = st.selectbox("Filter by Status", status_options)
    filtered_df = df.copy()
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df["priority"] == priority_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    st.subheader(f"Tickets ({len(filtered_df)} shown)")
    st.dataframe(filtered_df,width="stretch")

    csv = filtered_df.to_csv(index=False)
    st.download_button(
        "⬇️ Export filtered data as CSV",
        csv,
        "it_tickets_filtered.csv",
        "text/csv"
    )
    st.divider()
    priority_colors = {
        "Critical": "#ef4444",
        "High": "#f97316",
        "Medium": "#eab308",
        "Low": "#22c55e"
    }
    col1,col2 = st.columns(2)

    with col1:
        priority_counts = df["priority"].value_counts().reset_index()
        priority_counts.columns = ["priority","count"]
        fig = px.bar(
            priority_counts,
            "priority",
            "count",
            "priority",
            color_discrete_map=priority_colors,
            title="Tickets by Priority",
        )
        fig.update_layout(
            font_color="#e2e8f0",
            showlegend=False
        )
        st.plotly_chart(fig)
    with col2:
        avg_by_priority = df.groupby("priority")["resolution_time_hours"].mean().reset_index()
        avg_by_priority.columns = ["priority","avg_hours"]
        avg_by_priority["avg_hours"] = avg_by_priority["avg_hours"].round(1)
        fig2 = px.bar(
            avg_by_priority,
            "avg_hours",
            "priority",
            orientation="h",
            title="Avg Resolution Time by Priority (hours)",
            color_discrete_sequence=["#00d4ff"]
        )
        fig2.update_layout(
            font_color="#e2e8f0"
        )
        st.plotly_chart(fig2)

    Streamlit_render_ai_chat(df, "IT Tickets", chat_key="ITtickets_chat")
#Metadata Dashboard
def Render_Metadata():
    st.title("Dataset Metadata")
    df = get_all_metadatas(conn)
    st.dataframe(df)
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Export as CSV",csv,"datasets_metadata.csv","text/csv")
    # Pie chart - dataset size by rows
    fig = px.pie(
        df,
        "name",
        "rows",
        title="Dataset Size Distribution (by rows)",
    )
    st.plotly_chart(fig)
    Streamlit_render_ai_chat(df,"Dataset Metadata",chat_key="metadata_chat")

#Intelligence dashboard
def Render_Intelligence():
    st.title("🧠 Cross-Domain Intelligence")
    st.caption("AI-powered analysis across all three operational datasets simultaneously")
    st.divider()

    #Loading all three datasets
    df_incidents = get_all_cyber_incidents(conn)
    df_tickets = get_all_it_tickets(conn)
    df_metadata = get_all_metadatas(conn)

    #A Quick summary stats at the top
    col1, col2, col3 = st.columns(3)
    col1.metric("Cyber Incidents", len(df_incidents))
    col2.metric("IT Tickets", len(df_tickets))
    col3.metric("Datasets Tracked", len(df_metadata))

    st.divider()
    st.subheader("Select an Analysis")
    st.caption("Each analysis sends all three datasets to Gemini simultaneously for cross-domain insights.")

    #Initialising result in session state
    if "intelligence_result" not in st.session_state:
        st.session_state["intelligence_result"] = None
    if "intelligence_type" not in st.session_state:
        st.session_state["intelligence_type"] = None

    #analysis buttons — 2x2 grid for professional look instead of a list look
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔴 Identify High-Risk Periods", width="stretch"):
            with st.spinner("Analysing time related patterns across datasets..."): #spinner while data loads
                result = cross_dataset_analysis("high_risk", df_incidents, df_tickets, df_metadata)
            st.session_state["intelligence_result"] = result
            st.session_state["intelligence_type"] = "🔴 High-Risk Periods"

        if st.button("📊 Executive Threat Briefing", width="stretch"):
            with st.spinner("Generating executive briefing..."):
                result = cross_dataset_analysis("briefing", df_incidents, df_tickets, df_metadata)
            st.session_state["intelligence_result"] = result
            st.session_state["intelligence_type"] = "📊 Executive Threat Briefing"

    with col2:
        if st.button("🔗 Correlate Incidents with IT Tickets", width="stretch"):
            with st.spinner("Cross-referencing cybers incident and ticket patterns..."):
                result = cross_dataset_analysis("correlate", df_incidents, df_tickets, df_metadata)
            st.session_state["intelligence_result"] = result
            st.session_state["intelligence_type"] = "Cyber Incidents & Ticket Correlation"

        if st.button("🔍 Anomaly Detection", width="stretch"):
            with st.spinner("Scanning for anomalies across all domains..."):
                result = cross_dataset_analysis("anomaly", df_incidents, df_tickets, df_metadata)
            st.session_state["intelligence_result"] = result
            st.session_state["intelligence_type"] = "🔍 Anomaly Detection"

    #Results Display
    if st.session_state["intelligence_result"]:
        st.divider()
        st.subheader(f"Analysis Result — {st.session_state['intelligence_type']}")
        st.info(st.session_state["intelligence_result"])

        # Export result as text file
        st.download_button(
            label="⬇️ Export Analysis as Text",
            data=st.session_state["intelligence_result"],
            file_name=f"cortex_analysis_{st.session_state['intelligence_type'].replace(' ', '_')}.txt",
            mime="text/plain"
        )


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
            try:
                answer = ask_ai_about_data(user_question,df,dataset_name)
            except Exception as e:
                #Friendly error message for user on the GUI
                st.error("Sorry, the AI assistant is unavailable right now. Please try again later.") 
                #Technical error message for developer/debugger on terminal
                print(f"AI error: {e}")
                answer = None
        if answer:
            st.session_state[chat_key].append(("assistant",answer))
            st.rerun()
        
def Streamlit_main():
    if st.session_state["logged_in"]:
        User_Dashboard()
    else:
        Dashboard_Login_Register()

def main():
    Migrate_All_Tables()
    Initialise_Session()
    Streamlit_main()

if __name__ == "__main__":
    main()

conn.close() #closing the database connection when the program ends
    