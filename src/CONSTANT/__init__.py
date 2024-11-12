
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
import streamlit as st




load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION =  os.getenv('LOCATION')  
PROCESSOR_ID = os.getenv('PROCESSOR_ID') 
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
OPEN_AI_KEY = st.secrets['OPEN_AI_KEY']

credentials = service_account.Credentials.from_service_account_info(st.secrets["arjun_gcs_connection"])