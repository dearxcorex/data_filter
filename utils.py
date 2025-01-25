import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials



@st.cache_resource
def connect_to_gsheet():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(credentials)
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

 