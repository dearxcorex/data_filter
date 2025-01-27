import streamlit as st
import plotly.express as px
from utils import load_data
from datetime import datetime



# Set page config at the very start of your script
st.set_page_config(
    page_title="ระบบติดตามสถานีวิทยุ FM",  # Browser tab title
    page_icon="📻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Customize sidebar title
st.sidebar.markdown("""
    <style>
        [data-testid=stSidebar] [data-testid=stMarkdownContainer] {
            padding-top: 0rem;
        }
        .sidebar-title {
            font-size: 1.3rem;
            font-weight: bold;
            padding: 1rem 0;
            text-align: center;
            border-bottom: 2px solid #f0f2f6;
            margin-bottom: 1rem;
        }
    </style>
    <div class="sidebar-title">📻 ระบบติดตามสถานีวิทยุ FM</div>
    """, unsafe_allow_html=True)

# Rename pages in sidebar
st.sidebar.markdown("""
    <style>
        section[data-testid="stSidebar"] .css-17lntkn {
            display: none;
        }
        section[data-testid="stSidebar"] .css-pkbazv {
            font-size: 1rem;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)
def add_refresh_section():
    # st.sidebar.markdown('---')
    col1,col2 = st.sidebar.columns([2,1])

    with col1:
        st.markdown(f"🔄 ข้อมูลอัพเดทล่าสุด: {datetime.now().strftime('%H:%M:%S')}")

    with col2:
        if st.button('🔄 รีเฟรช'):
            st.cache_data.clear()
            st.rerun()

def show_statisticsshow_dashboard(df):

    add_refresh_section()

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

    #Add sidebar statistics 
    st.sidebar.markdown("---")
    not_applied = len(df[df['ยื่นคำขอ'] == 'ไม่ยื่น'])
    st.sidebar.write(f"จำนวนที่ไม่ยื่น: {not_applied}")

    #Option: Add percentage 
    not_applied_percentage = (not_applied/len(df)*100)
    st.sidebar.write(f"ร้อยละที่ไม่ยื่น: {not_applied_percentage:.1f}%")

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
        progress = (inspected / 200)
        st.progress(progress)
        st.write(f"ความคืบหน้า: {progress:.1%}")



def show_visualization(filtered_df):
    st.subheader("📊 Data Visualization")

    # Visualization type selector
    viz_type = st.selectbox(
        "Select Visualization Type",
        [ "District Summary", "Inspection Summary"]
    )

    if not filtered_df.empty:
        if viz_type == "District Summary":
            district_stats = filtered_df.groupby(['จังหวัด', 'อำเภอ']).agg({
                'ชื่อสถานี': 'count',
                'ยื่นคำขอ': lambda x: (x == 'ไม่ยื่น').sum(),
                'สถานะ': lambda x: (x == 'ตรวจแล้ว').sum()
            }).reset_index()
            district_stats.columns = ['จังหวัด', 'อำเภอ', 'จำนวนสถานีทั้งหมด','จำนวนที่ไม่ยื่น','จำนวนที่ตรวจแล้ว' ] 
            # district_stats['ร้อยละที่ตรวจแล้ว'] = (district_stats['จำนวนที่ตรวจแล้ว'] / district_stats['จำนวนสถานีทั้งหมด'] * 100).round(1)
            st.dataframe(district_stats, use_container_width=True)

def main():
    st.title('FM Radio Stations Dashboard')

    # Get data
    df = load_data()

    # Show dashboard
    show_statisticsshow_dashboard(df)
    show_visualization(df)

if __name__ == '__main__':
    main()