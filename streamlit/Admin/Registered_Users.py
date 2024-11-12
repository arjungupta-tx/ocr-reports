import streamlit as st
from src.SQLdb.sql_query_engine import fetch_all
import pandas as pd

# Replace with your actual database URL


# Function to fetch all users
# def fetch_all_users():
    
#     print(result)
    
#     data = [dict(row) for row in result]
#     return data

# # Function to delete a user by ID
# def delete_user(user_id):
#     # query = text("DELETE FROM users WHERE id = :user_id")
#     # with engine.connect() as connection:
#     #     connection.execute(query, {"user_id": user_id})
#     # st.success(f"User with ID {user_id} deleted successfully.")

# # Function to update a user's details
#     pass
# def update_user(user_id, new_username, new_is_active, new_role):
#     # query = text("""
#     #     UPDATE users 
#     #     SET username = :username, is_active = :is_active, role = :role 
#     #     WHERE id = :user_id
#     # """)
#     # with engine.connect() as connection:
#     #     connection.execute(query, {
#     #         "username": new_username,
#     #         "is_active": new_is_active,
#     #         "role": new_role,
#     #         "user_id": user_id
#     #     })
#     # st.success(f"User with ID {user_id} updated successfully.")
#      pass

# Display form to view, edit, and delete users
def display_users_form():
    st.write("### All Registered Users")
    columns = ["ID", "Name", "Email", "IsActive", "Username", "Password", "Role"]
    query = "Select Id_User,Name, Email, IsActive, UserName, Password, Role from User_Table"
    result = fetch_all(query)
    
    # Fetch all users
    
    
    if result:
        df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit
        st.write("### Registered Users")
        st.dataframe(df)  # or use st.table(df) for a static table
        # Convert to DataFrame for display
        # df = pd.DataFrame(users)
        # print(df)
        # st.dataframe(df)
        
        # Show each user's information and options to edit or delete
        # for idx, row in df.iterrows():
        #     st.write(f"**User ID {row['id']}: {row['username']}**")

        #     # Display user information with edit fields
        #     new_username = st.text_input(f"Username (ID {row['id']})", value=row['username'], key=f"username_{row['id']}")
        #     new_is_active = st.checkbox("Active", value=bool(row['is_active']), key=f"is_active_{row['id']}")
        #     new_role = st.selectbox("Role", options=["Admin", "User", "Guest"], index=["Admin", "User", "Guest"].index(row['role']), key=f"role_{row['id']}")

        #     # Buttons for update and delete actions
        #     col1, col2 = st.columns(2)
        #     with col1:
        #         if st.button("Update", key=f"update_{row['id']}"):
        #             update_user(row['id'], new_username, new_is_active, new_role)
        #             st.experimental_rerun()  # Refresh the app to show updated data
        #     with col2:
        #         if st.button("Delete", key=f"delete_{row['id']}"):
        #             delete_user(row['id'])
        #             st.experimental_rerun()  # Refresh the app to remove deleted user

    else:
        st.info("No users found.")

# Main function to run the app

    

display_users_form()
    
