import streamlit as st
from src.pipeline.userloging import userloging



def login_form():
    # Create the login form using st.form
    with st.form("Login Form", clear_on_submit=True):
        st.write("Login Form")
        
        # Username and password inputs
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Submit button
        submit_button = st.form_submit_button("Login")
        
        # Check if the form was submitted
        if submit_button:
            # Check if username and password are correct
            result = userloging(username.strip(),password.strip())
            if result is not None:
                st.success("Login successful!")
                st.session_state["logged_in"] = True  # Track login status with session state
                st.session_state["username"] = username
                
            
                return result