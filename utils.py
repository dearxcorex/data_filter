import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials



# @st.cache_resource
# def connect_to_gsheet():
#     scope = [
#         'https://www.googleapis.com/auth/spreadsheets',
#         'https://www.googleapis.com/auth/drive'
#     ]
#     credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
#     client = gspread.authorize(credentials)
#     return client
@st.cache_resource
def connect_to_gsheet():
    # Get the credentials from secrets
    credentials = {
        "type": st.secrets["gcp_service_account"]["type"],
        "project_id": st.secrets["gcp_service_account"]["project_id"],
        "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
        "private_key": st.secrets["gcp_service_account"]["private_key"],
        "client_email": st.secrets["gcp_service_account"]["client_email"],
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
        "universe_domain": st.secrets["gcp_service_account"]["universe_domain"]
    }
    
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_info(credentials, scopes=scope)
    client = gspread.authorize(creds)
    return client

@st.cache_data
def load_data():
    try:
        client = connect_to_gsheet()
        sheet = client.open('FM_Radio_Stations').worksheet('Sheet_1')
        df = pd.DataFrame(sheet.get_all_records())
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None 

 