import streamlit as st
import os
from pathlib import Path
# from src.streamlit.loging import login_form
from src.pipeline.userloging import userloging

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "User", "Admin"]


def login():

    # st.header("Log in")
    # role = st.selectbox("Choose your role", ROLES)
    with st.form("Login Form", clear_on_submit=True):
        st.write("Login Form")
        
        # Username and password inputs
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Submit button
        submit_button = st.form_submit_button("Login",use_container_width=True)
        
        # Check if the form was submitted
        if submit_button:
            # Check if username and password are correct
            result = userloging(username.strip(),password.strip())
            
            print(result)
            if result is not None:
                st.success("Login successful!")
                st.session_state["logged_in"] = True  # Track login status with session state
                st.session_state["user_id"] = result[0]
                st.session_state['permission'] = result[1]
                st.session_state['Isactive'] = result[2]
                st.session_state["user_email"] = result[3]
                st.session_state.role = result[4]
                st.rerun()
                

    # if st.button("Log in"):
    #     st.session_state.role = role
    #     st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page(os.path.join("streamlit","setting.py"), title="Settings", icon=":material/settings:")
user_1 = st.Page(
    Path("streamlit/User/ProcessPDF.py"),
    title="File management",
    icon=":material/help:",
    default=(role == "User"),
)
user_2 = st.Page(os.path.join("streamlit/User","Project.py"), title="Project", icon=":material/handyman:"
)

user_3 = st.Page(os.path.join("streamlit/User","FileProcessiong.py"),title="File Processing", icon=":material/handyman:")

admin_1 = st.Page(
    os.path.join("streamlit/Admin","Admin_Setting.py"),
    title="Admin Setting",
    icon=":material/security:",
    default=(role == "Admin"),
)
admin_2 = st.Page(os.path.join("streamlit/Admin","User_Registraton.py"), title="User Registraton",icon=":material/person_add:" )
admin_3 = st.Page(os.path.join("streamlit/Admin","Registered_Users.py"), title="Rgistered User List",icon=":material/person_add:" )

account_pages = [logout_page, settings]
user_page = [user_2, user_1]

admin_pages = [admin_1, admin_2]

# st.title("Request man")
# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.role in ["User", "Admin"]:
    page_dict["MOR"] = user_page

if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()