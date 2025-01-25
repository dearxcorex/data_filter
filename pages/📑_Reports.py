import streamlit as st
import pandas as pd
from utils import load_data



def show_reports():
    st.title('FM Radio Stations Reports')

    # Get data
    df = load_data()

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
    st.sidebar.subheader('สถานะการตรวจปี 2567')
    show_inspected = st.sidebar.checkbox('ตรวจปี 2567 แล้ว', value=False)
    show_not_inspected = st.sidebar.checkbox('ยังไม่ได้ตรวจ', value=False)

    # Filter data
    filtered_df = df.copy()
    if selected_province != 'ALL':
        filtered_df = filtered_df[filtered_df['จังหวัด'] == selected_province]
    if selected_district != 'ALL':
        filtered_df = filtered_df[filtered_df['อำเภอ'] == selected_district]
 
    # Status filter for 2568
    st.sidebar.subheader('สถานะการตรวจปี 2568')
    status_options = df['สถานะ'].unique()
    selected_status = st.sidebar.radio(':)', status_options, index=0)

    if selected_status:
        filtered_df = filtered_df[filtered_df['สถานะ'] == selected_status]

    # Filter by inspection status
    st.caption('Table Filter')
    status_conditions = []
    if show_inspected:
        status_conditions.append(filtered_df['ตรวจสอบมาตรฐาน 2567'] == 'ตรงตามมาตรฐาน')
    if show_not_inspected:
        status_conditions.append(filtered_df['ตรวจสอบมาตรฐาน 2567'] == "ยังไม่ตรวจ")

    if status_conditions:
        filtered_df = filtered_df[pd.concat(status_conditions, axis=1).any(axis=1)]

    # Display filtered data
    st.dataframe(filtered_df)

    # Show statistics in sidebar
    st.sidebar.write(f'จำนวนสถานีทั้งหมด: {len(filtered_df)}')


def main():
    show_reports()

if __name__ == '__main__':
    main()