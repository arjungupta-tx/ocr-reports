from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

# initialize Connector object
connector = Connector()

# connection_sql = st.secrets["database"]['connection']
# driver_sql = st.secrets["database"]['driver']
# user_sql= st.secrets["database"]['user']
# password_sql = st.secrets["database"]['password']
# database_sql = st.secrets["database"]['database']


connection_sql = os.getenv("connection")
driver_sql = os.getenv("driver")
user_sql= os.getenv("user")
password_sql = os.getenv("password")
database_sql = os.getenv("database")

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        connection_sql,
        driver_sql,
        user = user_sql,
        password=password_sql,
        database = database_sql
        
    )

    return conn