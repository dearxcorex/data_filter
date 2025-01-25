import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
from utils import load_data  # Import the utility function







def show_map_visualization(df):
    st.subheader("🗺️ แผนที่แสดงสถานีวิทยุ 3 จังหวัด")


  
    
    m = folium.Map(
        location=[15.0000, 102.0000],
        zoom_start=8,
        tiles ='CartoDB positron',
        )
    

    #create marker cluster
    inspected_cluster = folium.FeatureGroup(name='✅ ตรวจแล้ว')
    not_inspected_cluster = folium.FeatureGroup(name='⏳ ยังไม่ตรวจ')


    #add markers
    for idx,row in df.iterrows():
        if pd.notna(row['ละติจูด']) and pd.notna(row['ลองจิจูด']):
            popup_content = f"""
            <div style="font-family:'Sarabun', sans-serif; font-size:14px;">
            <b>ชื่อสถานี:</b> {row['ชื่อสถานี']}<br>
            <b>ความถี่:</b> {row['ความถี่']} MHz<br>
            <b>จังหวัด:</b> {row['จังหวัด']}<br>
            <b>อำเภอ:</b> {row['อำเภอ']}<br>
            <b>สถานะ:</b> {row['สถานะ']}
            </div>
            """

            if row['สถานะ'] == 'ตรวจแล้ว':
                icon_color = 'green'
                marker_group = inspected_cluster
            else:
                icon_color = 'red'
                marker_group = not_inspected_cluster

            folium.CircleMarker(
                location=[row['ละติจูด'], row['ลองจิจูด']],
                radius=8,
                popup=folium.Popup(popup_content, max_width=300),
                color=icon_color,
                fill=True,
                fill_color=icon_color,
                fill_opacity=0.7,
                weight=2,
                tooltip=row['ชื่อสถานี']

            ).add_to(marker_group)

    inspected_cluster.add_to(m)
    not_inspected_cluster.add_to(m)
    folium.LayerControl().add_to(m)
    folium.LatLngPopup().add_to(m)
     # Display map
    try:
        folium_static(m)
    except Exception as e:
        st.error(f"Error displaying map: {str(e)}")
    #Statistics
    # col1, col2 = st.columns(2)

    # with col1:
    #         st.subheader("📊 สรุปรายจังหวัด")
    #         province_summary = df.groupby('จังหวัด').agg({
    #             'ชื่อสถานี': 'count',
    #             'สถานะ': lambda x: (x == 'ตรวจแล้ว').sum()
    #         }).reset_index()
            
    #         province_summary.columns = ['จังหวัด', 'จำนวนสถานีทั้งหมด', 'จำนวนที่ตรวจแล้ว']
    #         province_summary['ร้อยละที่ตรวจแล้ว'] = (province_summary['จำนวนที่ตรวจแล้ว'] / province_summary['จำนวนสถานีทั้งหมด'] * 100).round(1)
    #         st.dataframe(province_summary, use_container_width=True)

    # with col2:
    #     st.subheader("📈 สัดส่วนการตรวจสอบ")
    #     status_counts = df['สถานะ'].value_counts()
    #     fig = px.pie(
    #         values=status_counts.values,
    #         names=status_counts.index,
    #         title='สัดส่วนสถานะการตรวจสอบ',
    #         hole=0.4,
    #         color_discrete_map={'ตรวจแล้ว': '#00CC96', 'ยังไม่ตรวจ': '#EF553B'}
    #     )
    #     st.plotly_chart(fig, use_container_width=True)


def main():
    st.title('🗺️ แผนที่แสดงสถานีวิทยุ')

    # Load data using utility function
    df = load_data()
    
    if df is not None:
        # Filter for specific provinces
        provinces_of_interest = ['ชัยภูมิ', 'นครราชสีมา', 'บุรีรัมย์']
        filtered_df = df[df['จังหวัด'].isin(provinces_of_interest)]
        
        # Filters
        st.sidebar.header('🔍 ตัวกรองข้อมูล')
        selected_provinces = st.sidebar.multiselect(
            'เลือกจังหวัด',
            provinces_of_interest,
            default=provinces_of_interest
        )
        
        status_filter = st.sidebar.multiselect(
            'สถานะการตรวจสอบ',
            ['ตรวจแล้ว', 'ยังไม่ตรวจ'],
            default=['ตรวจแล้ว', 'ยังไม่ตรวจ']
        )
        
        # Apply filters
        map_df = filtered_df[
            (filtered_df['จังหวัด'].isin(selected_provinces)) &
            (filtered_df['สถานะ'].isin(status_filter))
        ]
        
        if not map_df.empty:
            show_map_visualization(map_df)
            
            # Summary
            st.sidebar.markdown('---')
            st.sidebar.subheader('📊 สรุปข้อมูล')
            st.sidebar.write(f'จำนวนสถานีทั้งหมด: {len(map_df)}')
            st.sidebar.write(f'จำนวนที่ตรวจแล้ว: {len(map_df[map_df["สถานะ"] == "ตรวจแล้ว"])}')
            st.sidebar.write(f'จำนวนที่ยังไม่ตรวจ: {len(map_df[map_df["สถานะ"] == "ยังไม่ตรวจ"])}')
        else:
            st.warning('⚠️ ไม่พบข้อมูลสำหรับเงื่อนไขที่เลือก')

   

if __name__ == "__main__":
    main()
