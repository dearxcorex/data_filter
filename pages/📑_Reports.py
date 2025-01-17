import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Configure Google Sheets connection
@st.cache_resource
def connect_to_gsheet():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(credentials)
    return client

def show_reports():
    st.title('FM Radio Stations Reports')

    # Get data
    client = connect_to_gsheet()
    sheet = client.open('FM_Radio_Stations').worksheet('Sheet_1')
    df = pd.DataFrame(sheet.get_all_records())

    # Sidebar filters
    st.sidebar.header('Filter Data')
    provinces = ['ALL'] + sorted(df['จังหวัด'].unique().tolist())
    selected_province = st.sidebar.selectbox('Select Province', provinces)

    # Show district dropdown only if province is selected
    if selected_province != 'ALL':
        province_districts = df[df['จังหวัด'] == selected_province]['อำเภอ'].unique()
        districes = ['ALL'] + sorted(province_districts.tolist())
        selected_district = st.sidebar.selectbox('Select District', districes, index=0)
    else:
        selected_district = 'ALL'

    # Inspection status checkboxes
    st.sidebar.subheader('Inspection Unwanted Emissions Status')
    show_inspected = st.sidebar.checkbox('ตรวจปี 2567 แล้ว', value=False)
    show_not_inspected = st.sidebar.checkbox('ยังไม่ได้ตรวจ', value=False)

    # Filter data
    filtered_df = df.copy()
    if selected_province != 'ALL':
        filtered_df = filtered_df[filtered_df['จังหวัด'] == selected_province]
    if selected_district != 'ALL':
        filtered_df = filtered_df[filtered_df['อำเภอ'] == selected_district]

    # Status filter for 2568
    st.sidebar.subheader('Inspection Status 2568')
    status_options = df['สถานะ'].unique()
    selected_status = st.sidebar.radio(':)', status_options, index=0)

    if selected_status:
        filtered_df = filtered_df[filtered_df['สถานะ'] == selected_status]

    # Filter by inspection status
    st.caption('ตรวจการแพร่แปลกปลอม')
    status_conditions = []
    if show_inspected:
        status_conditions.append(filtered_df['ตรวจการแพร่แปลกปลอม'] == 'ตรวจปี 2567 แล้ว')
    if show_not_inspected:
        status_conditions.append(filtered_df['ตรวจการแพร่แปลกปลอม'] == 'ยังไม่ตรวจ')

    if status_conditions:
        filtered_df = filtered_df[pd.concat(status_conditions, axis=1).any(axis=1)]

    # Display filtered data
    st.dataframe(filtered_df)

    # Show statistics in sidebar
    total_stations = len(filtered_df)
    st.sidebar.write(f'จำนวนสถานีทั้งหมด: {total_stations}')
    
    if total_stations > 0:
        inspected = len(filtered_df[filtered_df['ตรวจการแพร่แปลกปลอม'] == 'ตรวจปี 2567 แล้ว'])
        not_inspected = len(filtered_df[filtered_df['ตรวจการแพร่แปลกปลอม'] == 'ยังไม่ตรวจ'])

        st.sidebar.write(f'จำนวนสถานีที่ตรวจปี 2567 แล้ว: {inspected}')
        st.sidebar.write(f'จำนวนสถานีที่ยังไม่ตรวจ: {not_inspected}')

if __name__ == '__main__':
    show_reports()