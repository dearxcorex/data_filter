import folium.plugins
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from utils import load_data  # Import the utility function

from folium import plugins
import streamlit.components.v1 as components







def show_map_visualization(df):
    df = df.copy()
        # Create a styled legend
    legend_html = """
    <style>
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .circle {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 10px;
            display: inline-block;
        }
    </style>
    
    <div style="font-family: 'Sarabun', sans-serif;">
        <div class="legend-item">
            <span class="circle" style="background-color: green;"></span>
            <span>✅ สถานีที่ยื่นคำขอและตรวจแล้ว</span>
        </div>
        <div class="legend-item">
            <span class="circle" style="background-color: red;"></span>
            <span>⏳ สถานีที่ยื่นคำขอแต่ยังไม่ได้ตรวจ</span>
        </div>
        <div class="legend-item">
            <span class="circle" style="background-color: black;"></span>
            <span>⚠️ สถานีที่ไม่ยื่นคำขอและยังไม่ได้ตรวจ</span>
        </div>
        <div class="legend-item">
            <span class="circle" style="background-color: blue;"></span>
            <span>📋 สถานีที่ไม่ยื่นคำขอแต่ตรวจแล้ว</span>
        </div>
    </div>
    """
    
    st.sidebar.markdown(legend_html, unsafe_allow_html=True)
    
  


  
    
    m = folium.Map(
        location=[15.0000, 102.0000],
        zoom_start=5,
        tiles ='CartoDB positron',
        prefer_canvas=True,
        )
    
    df['coord_pair'] = df.apply(lambda row:
                                f"{row['ละติจูด']},{row['ลองจิจูด']}"
                                if pd.notna(row['ละติจูด']) and pd.notna(row['ลองจิจูด'])
                                else "missing",
                                axis=1)
    coord_count = df['coord_pair'].value_counts()
    duplicate_coords = coord_count[coord_count > 1].index.tolist()
    

    #add smooth zoom control
    # folium.plugins.SmoothWheelZoom().add_to(m)

    plugins.LocateControl(
        auto_start=False,
        KeepCurrentZoomLevel=True,
        strings={'title':'ตำแหน่งของคุณ'},
        position="topleft",
        flyTo=False,
        drawCircle=True,
        showPopup=True,
        locate_options={
            'enableHighAccuracy':True,
            'watch':True,
            'timeout':10000,
            'maximumAge':0,
            'setView':'untilPan',
        }
    ).add_to(m)




    #create marker cluster
    inspected_cluster = folium.FeatureGroup(name='✅ ตรวจแล้ว')
    not_inspected_cluster = folium.FeatureGroup(name='⏳ ยังไม่ตรวจ')
    not_apply_cluster = folium.FeatureGroup(name='🔍 ไม่ยื่นคำขอตรวจแล้ว')
    not_apply_cluster_2 = folium.FeatureGroup(name='🔍 ไม่ยื่นคำขอยังไม่ตรวจ')

    for coord_pair in df['coord_pair'].unique():
        if coord_pair == "missing":
            continue
            
        lat, lon = map(float, coord_pair.split(','))
        stations_at_location = df[df['coord_pair'] == coord_pair]
        
        # Check if this is a duplicate location
        is_duplicate = coord_pair in duplicate_coords
        
        # Create popup content
        if is_duplicate:
            # For duplicate locations, show all stations
            popup_content = f"""
            <div style="font-family:'Sarabun', sans-serif; font-size:14px;">
            <b>⚠️ พบ {len(stations_at_location)} สถานีที่มีพิกัดเดียวกัน:</b><br><br>
            """
            
            for idx, row in stations_at_location.iterrows():
                popup_content += f"""
                <div style="margin-bottom:10px; padding-bottom:10px; border-bottom:1px solid #eee;">
                <b>ชื่อสถานี:</b> {row['ชื่อสถานี']}<br>
                <b>ความถี่:</b> {row['ความถี่']} MHz<br>
                <b>จังหวัด:</b> {row['จังหวัด']}<br>
                <b>อำเภอ:</b> {row['อำเภอ']}<br>
                <b>สถานะ:</b> {row['สถานะ']}
                </div>
                """
                
            popup_content += f"""
            <a href="https://www.google.com/maps/dir/?api=1&destination={lat},{lon}" 
               target="_blank" style="
                background-color: #4285F4;
                color: white;
                padding: 8px 12px;
                text-decoration: none;
                border-radius: 4px;
                display: inline-block;
                margin-top: 5px;
            ">
            🚗 นำทาง
            </a>
            </div>
            """
            
            # Use a special icon for duplicate locations
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                popup=folium.Popup(popup_content, max_width=350),
                color='purple',  # Special color for duplicates
                fill=True,
                fill_color='purple',
                fill_opacity=0.7,
                weight=2,
                tooltip=f"⚠️ {len(stations_at_location)} สถานีที่พิกัดเดียวกัน"
            ).add_to(m)
            
        else:
            # For single locations, use your existing code
            row = stations_at_location.iloc[0]
            
            popup_content = f"""
            <div style="font-family:'Sarabun', sans-serif; font-size:14px;">
            <b>ชื่อสถานี:</b> {row['ชื่อสถานี']}<br>
            <b>ความถี่:</b> {row['ความถี่']} MHz<br>
            <b>จังหวัด:</b> {row['จังหวัด']}<br>
            <b>อำเภอ:</b> {row['อำเภอ']}<br>
            <b>สถานะ:</b> {row['สถานะ']}
            <br>
            <a href="https://www.google.com/maps/dir/?api=1&destination={lat},{lon}" 
               target="_blank" style="
                background-color: #4285F4;
                color: white;
                padding: 8px 12px;
                text-decoration: none;
                border-radius: 4px;
                display: inline-block;
                margin-top: 5px;
            ">
            🚗 นำทาง
            </a>
            </div>
            """
            
            # Determine marker color based on your existing logic
            if row['ยื่นคำขอ'] == 'ไม่ยื่น' and row['สถานะ'] == 'ยังไม่ตรวจ':
                icon_color = 'black'
                marker_group = not_apply_cluster_2
            elif row['ยื่นคำขอ'] == 'ไม่ยื่น' and row['สถานะ'] == 'ตรวจแล้ว':
                icon_color = 'blue'
                marker_group = not_apply_cluster
            elif row['สถานะ'] == 'ยังไม่ตรวจ':
                icon_color = 'red'
                marker_group = not_inspected_cluster
            elif row['สถานะ'] == 'ตรวจแล้ว':
                icon_color = 'green'
                marker_group = inspected_cluster
            
            folium.CircleMarker(
                location=[lat, lon],
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
    not_apply_cluster.add_to(m)
    not_apply_cluster_2.add_to(m)
    folium.LayerControl().add_to(m)
    folium.LatLngPopup().add_to(m)
    
    #add fullscreen button
    plugins.Fullscreen(
        position='topleft',
        title='Full Screen',
        title_cancel='Exit Full Screen',
        force_separate_button=True,
    ).add_to(m)

 

    #Display map
    st_map = st_folium(
        m, 
        width= 1000,
        height=700,
        returned_objects=['last_clicked'],
        use_container_width=True,
        key='main_map',
        )

    # Optional: Display a summary of duplicate locations
    if duplicate_coords and duplicate_coords[0] != "missing":
        with st.expander("⚠️ สถานีที่มีพิกัดซ้ำกัน"):
            for coord in duplicate_coords:
                if coord == "missing":
                    continue
                stations = df[df['coord_pair'] == coord]
                st.write(f"**พิกัด: {coord}** - {len(stations)} สถานี:")
                st.dataframe(stations[['ชื่อสถานี', 'ความถี่', 'จังหวัด', 'อำเภอ']])






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
            'สถานะการตรวจสอบปี68',
            ['ตรวจแล้ว', 'ยังไม่ตรวจ'],
            default=['ยังไม่ตรวจ']
        )
        status_filter_67 = st.sidebar.multiselect(
            'สถานะการตรวจสอบปี 67',
            ['ตรงตามมาตรฐาน', 'ยังไม่ตรวจ'],
            default=['ยังไม่ตรวจ']
        )
        # Apply filters
        map_df = filtered_df[
            (filtered_df['จังหวัด'].isin(selected_provinces)) &
            (filtered_df['สถานะ'].isin(status_filter)) &
            (filtered_df['ตรวจสอบมาตรฐาน 2567'].isin(status_filter_67))
        ]
        
        if not map_df.empty:
            show_map_visualization(map_df)
            
            # Summary
            st.sidebar.markdown('---')
            st.sidebar.subheader('📊 สรุปข้อมูล')
            st.sidebar.write(f'จำนวนสถานีทั้งหมด: {len(map_df)}')
            st.sidebar.write(f'จำนวนที่ตรวจแล้ว: {len(map_df[map_df["สถานะ"] == "ตรวจแล้ว"])}')
            st.sidebar.write(f'จำนวนที่ยังไม่ตรวจ: {len(map_df[map_df["สถานะ"] == "ยังไม่ตรวจ"])}')
            st.sidebar.write(f'จำนวนที่ยังไม่ตรวจปี 2567: {len(map_df[map_df["ตรวจสอบมาตรฐาน 2567"] == "ยังไม่ตรวจ"])}')
        else:
            st.warning('⚠️ ไม่พบข้อมูลสำหรับเงื่อนไขที่เลือก')

   

if __name__ == "__main__":
    main()
