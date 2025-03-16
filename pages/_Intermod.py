import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance

def find_potential_intermod(df, target_freq, lat, lon, distance_threshold=100):
    """Find potential intermodulation products within specified distance"""
    # Convert frequency columns to numeric, removing any non-numeric characters
    df['ความถี่'] = pd.to_numeric(df['ความถี่'].astype(str).str.replace('[^\d.]', ''), errors='coerce')
    
    # Calculate distance for all stations
    df['distance'] = df.apply(
        lambda row: calculate_distance(lat, lon, 
                                    float(row['ละติจูด']) if pd.notnull(row['ละติจูด']) else 0,
                                    float(row['ลองจิจูด']) if pd.notnull(row['ลองจิจูด']) else 0),
        axis=1
    )
    
    # Filter stations within distance threshold
    nearby_stations = df[df['distance'] <= distance_threshold].copy()
    
    # Find potential intermodulation products
    results = []
    n = len(nearby_stations)
    
    for i in range(n):
        for j in range(i+1, n):
            f1 = nearby_stations.iloc[i]['ความถี่']
            f2 = nearby_stations.iloc[j]['ความถี่']
            
            # Check for common intermodulation products
            im_products = [
                2*f1 - f2,      # Third-order (2A-B)
                2*f2 - f1,      # Third-order (2B-A)
                3*f1 - 2*f2,    # Fifth-order (3A-2B)
                3*f2 - 2*f1,    # Fifth-order (3B-2A)
                f1 + f2,        # Second-order sum (A+B)
                abs(f1 - f2),   # Second-order difference |A-B|
                2*f1 + f2,      # Third-order sum (2A+B)
                f1 + 2*f2,      # Third-order sum (A+2B)
                2*(f1 + f2),    # Fourth-order (2(A+B))
                3*f1,           # Third harmonic of f1
                3*f2,           # Third harmonic of f2
                4*f1,           # Fourth harmonic of f1
                4*f2,           # Fourth harmonic of f2
                5*f1,           # Fifth harmonic of f1
                5*f2           # Fifth harmonic of f2
            ]
            
            for im_freq in im_products:
                if abs(im_freq - target_freq) <= 0.1:  # Within 0.1 MHz tolerance
                    # Determine the order type
                    if im_freq in [f1 + f2, abs(f1 - f2)]:
                        order = "Second-order"
                    elif im_freq in [2*f1 - f2, 2*f2 - f1, 2*f1 + f2, f1 + 2*f2, 3*f1, 3*f2]:
                        order = "Third-order"
                    elif im_freq in [2*(f1 + f2), 4*f1, 4*f2]:
                        order = "Fourth-order"
                    elif im_freq in [3*f1 - 2*f2, 3*f2 - 2*f1, 5*f1, 5*f2]:
                        order = "Fifth-order"
                    
                    results.append({
                        'Order': order,
                        'Station1': nearby_stations.iloc[i]['ชื่อสถานี'],
                        'Freq1': f1,
                        'Province1': nearby_stations.iloc[i]['จังหวัด'],
                        'District1': nearby_stations.iloc[i]['อำเภอ'],
                        'Station2': nearby_stations.iloc[j]['ชื่อสถานี'],
                        'Freq2': f2,
                        'Province2': nearby_stations.iloc[j]['จังหวัด'],
                        'District2': nearby_stations.iloc[j]['อำเภอ'],
                        'Intermod_Freq': im_freq,
                        'Distance1': nearby_stations.iloc[i]['distance'],
                        'Distance2': nearby_stations.iloc[j]['distance']
                    })
    
    return pd.DataFrame(results)

def main():
    st.title("📻 Intermodulation Analysis")
    
    # Load data
    df = load_data()
    
    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_freq = st.number_input("Target Frequency (MHz)", value=126.4, step=0.1,format="%.3f")
    
    with col2:
        latitude = st.number_input("Latitude", value=15.05422,format="%.5f")
    
    with col3:
        longitude = st.number_input("Longitude", value=103.03137,format="%.5f")
    
    
    if st.button("Analyze Intermodulation"):
        results = find_potential_intermod(df, target_freq, latitude, longitude )
        
        if len(results) > 0:
            st.subheader("Potential Intermodulation Products Found:")
            st.dataframe(results)
        else:
            st.info("No potential intermodulation products found within the specified radius.")

if __name__ == "__main__":
    main()
