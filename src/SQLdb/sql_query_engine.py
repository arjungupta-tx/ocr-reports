# from src.SQLdb.sql_connection import getconn
import sqlalchemy
from sqlalchemy import create_engine, text
import streamlit as st
from google.cloud.sql.connector import Connector
import sqlalchemy

import pymysql
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
# import streamlit as st

credentials = service_account.Credentials.from_service_account_info(st.secrets["arjun_gcs_connection"])
load_dotenv()

# initialize Connector object
connector = Connector(credentials=credentials)

connection_sql = st.secrets["database"]['connection']
driver_sql = st.secrets["database"]['driver']
user_sql= st.secrets["database"]['user']
password_sql = st.secrets["database"]['password']
database_sql = st.secrets["database"]['database']


# connection_sql = os.getenv("connection")
# driver_sql = os.getenv("driver")
# user_sql= os.getenv("user")
# password_sql = os.getenv("password")
# database_sql = os.getenv("database")

# def init_connection():
#     """Initializes a connection to the Cloud SQL database using SQLAlchemy."""
#     try:
#         # Using the Cloud SQL Proxy
#         engine = create_engine(
#             f"mysql+pymysql://{user_sql}:{password_sql}@/cloudsql/{connection_sql}/{database_sql}"
#         )
#         return engine
#     except Exception as e:
#         st.error(f"Error connecting to MySQL using SQLAlchemy: {e}")
#         return None
    
# @st.cache_resource
# def init_connection() -> Engine:
#     """Initializes a connection to the Cloud SQL database using SQLAlchemy."""
#     try:
#         # Format the connection string for Cloud SQL using SQLAlchemy and MySQL connector
#         engine = create_engine(
#             f"mysql+mysqlconnector://{user_sql}:{password_sql}@/{database_sql}"
#             f"?unix_socket=/cloudsql/{connection_sql}"
#         )
#         return engine
#     except Exception as e:
#         st.error(f"Error connecting to MySQL using SQLAlchemy: {e}")
#         return None
# engine = init_connection()    

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



engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def insert_data(sql_query):
    """Executes an INSERT SQL statement and returns success confirmation."""
    try:
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(sql_query))
            connection.commit()
            print("Data Inserted successfully")
            return {"last_row_id": result.lastrowid, "rows_affected": result.rowcount}
    except Exception as e:
        print("An error occurred during insertion:", e)
        # return {"status": "error", "message": str(e)}

def execute_update(sql_query):
    """Executes an UPDATE SQL statement and returns success confirmation."""
    try:
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(sql_query))
            connection.commit()
            return {"status": "success", "rows_affected": result.rowcount}
    except Exception as e:
        print("An error occurred during update:", e)
        # return {"status": "error", "message": str(e)}
    
def execute_delete(sql_query):
    """Executes a DELETE SQL statement and returns success confirmation."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            connection.commit()
            return {"status": "success", "rows_affected": result.rowcount}
    except Exception as e:
        print("An error occurred during deletion:", e)
        # return {"status": "error", "message": str(e)}
    



def fetch_all(sql_query):
    """Fetches all results from a SELECT query."""
    try:
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(sql_query))
            data = result.fetchall()
            return data
    except Exception as e:
        print("An error occurred while fetching all records:", e)
        return None

def fetch_one(sql_query):
    """Fetches a single result from a SELECT query."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            data = result.fetchone()
            return data
    except Exception as e:
        print("An error occurred while fetching one record:", e)
        return None

def fetch_many(sql_query, size):
    """Fetches a specific number of rows from a SELECT query."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            data = result.fetchmany(size)
            return data
    except Exception as e:
        print("An error occurred while fetching many records:", e)
        return None    
    

