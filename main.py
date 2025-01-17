import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
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

def show_statisticsshow_dashboard(df):
    # Create three columns for statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_stations = len(df)
        st.metric(
            label="จำนวนสถานีทั้งหมด",
            value=total_stations
        )
        
    with col2:
        inspected = len(df[df['สถานะ'] == 'ตรวจแล้ว'])
        st.metric(
            label="ตรวจแล้ว ปี 2568",
            value=inspected,
            delta=f"{(inspected/len(df)*100):.1f}%"
        )
        
    with col3:
        not_inspected = len(df[df['สถานะ'] == 'ยังไม่ตรวจ'])
        st.metric(
            label="ยังไม่ได้ตรวจ ปี 2568",
            value=not_inspected,
            delta=f"{(not_inspected/len(df)*100):.1f}%"
        )

    # Add province-wise statistics
    st.subheader("สถิติรายจังหวัดสถานีที่ตรวจแล้ว")
    province_stats = df.groupby('จังหวัด').agg({
        'ชื่อสถานี': 'count',
        'สถานะ': lambda x: (x == 'ตรวจแล้ว').sum()
    }).reset_index()
    province_stats.columns = ['จังหวัด', 'จำนวนสถานีทั้งหมด', 'จำนวนที่ตรวจแล้ว']
    province_stats['ร้อยละที่ตรวจแล้ว'] = (province_stats['จำนวนที่ตรวจแล้ว'] / province_stats['จำนวนสถานีทั้งหมด'] * 100).round(1)
    st.dataframe(province_stats, use_container_width=True)


    # # Display province statistics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Add a chart showing inspection progress
        st.subheader("ความคืบหน้าการตรวจสอบ")
        progress = (inspected / total_stations)
        st.progress(progress)
        st.write(f"ความคืบหน้า: {progress:.1%}")
def main():
    st.title('FM Radio Stations Dashboard')

    # Get data
    client = connect_to_gsheet()
    sheet = client.open('FM_Radio_Stations').worksheet('Sheet_1')
    df = pd.DataFrame(sheet.get_all_records())

    # Show dashboard
    show_statisticsshow_dashboard(df)


if __name__ == '__main__':
    main()