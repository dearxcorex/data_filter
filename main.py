import streamlit as st
import plotly.express as px
from utils import load_data


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
                'สถานะ': lambda x: (x == 'ตรวจแล้ว').sum()
            }).reset_index()
            district_stats.columns = ['จังหวัด', 'อำเภอ', 'จำนวนสถานีทั้งหมด', 'จำนวนที่ตรวจแล้ว'] 
            district_stats['ร้อยละที่ตรวจแล้ว'] = (district_stats['จำนวนที่ตรวจแล้ว'] / district_stats['จำนวนสถานีทั้งหมด'] * 100).round(1)
            st.dataframe(district_stats, use_container_width=True)

            fig = px.bar(
                district_stats,
                x='อำเภอ',
                y='จำนวนสถานีทั้งหมด',
                color='ร้อยละที่ตรวจแล้ว',
                facet_col='จังหวัด',
                facet_col_wrap=2,  # Number of columns in the facet grid
                title='สรุปจำนวนสถานีรายอำเภอ',
                color_continuous_scale='RdYlGn',
                height=700,  # Adjust height as needed
              
            )
            fig.update_xaxes(tickangle=45)
            fig.update_layout(
                showlegend=True,
                margin = dict(t=100,l=50,r=50,b=100)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            status_count = filtered_df['สถานะ'].value_counts()
            fig = px.pie(
                values=status_count.values,
                names=status_count.index,
                title='สัดส่วนสถานะการตรวจสอบสถานี',
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
def main():
    st.title('FM Radio Stations Dashboard')

    # Get data
    df = load_data()

    # Show dashboard
    show_statisticsshow_dashboard(df)
    show_visualization(df)

if __name__ == '__main__':
    main()