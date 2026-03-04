import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Import our custom engine modules
from src.data_generator import generate_logistics_data
from src.dist_calc import create_distance_matrix
from src.optimizer import solve_cvrp

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="Logistics Engine")
st.title("🚚 Intelligent Logistics Engine")
st.markdown("Supply Chain Optimization using Google OR-Tools")

# --- Sidebar Controls ---
st.sidebar.header("Optimization Parameters")
num_orders = st.sidebar.slider("Number of Deliveries", 10, 100, 30)
num_vehicles = st.sidebar.slider("Number of Vehicles", 1, 10, 3)
vehicle_capacity = st.sidebar.slider("Vehicle Capacity (kg)", 50, 500, 150)

# Central Warehouse Coordinates
HUB_LAT, HUB_LON = 12.9165, 79.1325

# --- Main Application Logic ---
if st.sidebar.button("Generate & Optimize Routes"):
    
    with st.spinner("1. Generating Synthetic Order Data..."):
        df_orders = generate_logistics_data(num_orders, HUB_LAT, HUB_LON, radius_km=15)
        # Add the Hub as the starting point
        hub_data = pd.DataFrame([{'Order_ID': 'HUB', 'Latitude': HUB_LAT, 'Longitude': HUB_LON, 'Delivery_Weight_kg': 0}])
        logistics_df = pd.concat([hub_data, df_orders], ignore_index=True)
        
        st.write("### 📦 Delivery Nodes Generated", logistics_df.head())

    with st.spinner("2. Calculating Matrix & Running OR-Tools Engine..."):
        dist_matrix = create_distance_matrix(logistics_df)
        
        # We multiply by 1000 to convert km to meters. 
        # OR-Tools requires integers, so we do this to prevent losing precision!
        dist_matrix_meters = dist_matrix * 1000 
        
        demands = logistics_df['Delivery_Weight_kg'].tolist()
        
        # Call our Brain
        routes = solve_cvrp(dist_matrix_meters, demands, num_vehicles, vehicle_capacity)

    # --- Visualization ---
    if routes:
        st.success("✅ Optimal Routes Calculated Successfully!")
        
        # --- NEW: CALCULATE BUSINESS KPIs ---
        total_distance_km = 0
        total_payload_kg = 0
        vehicles_used = 0
        
        for route in routes:
            # A route is only 'used' if it has more than just [0, 0] (Hub to Hub)
            if len(route) > 2: 
                vehicles_used += 1
                for i in range(len(route) - 1):
                    from_node = route[i]
                    to_node = route[i+1]
                    # Look up the exact distance in our matrix
                    total_distance_km += dist_matrix[from_node][to_node]
                    
                    # Add to payload if it's a delivery node (not the hub)
                    if to_node != 0: 
                        total_payload_kg += demands[to_node]
                        
        # --- NEW: DISPLAY STREAMLIT METRICS ---
        st.markdown("### 📊 Optimization KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="🚚 Vehicles Utilized", value=f"{vehicles_used} / {num_vehicles}")
        col2.metric(label="📏 Total Distance Driven", value=f"{total_distance_km:.2f} km")
        col3.metric(label="📦 Total Payload Delivered", value=f"{total_payload_kg} kg")
        st.markdown("---")
        
        # Create a Folium map centered on the Hub
        m = folium.Map(location=[HUB_LAT, HUB_LON], zoom_start=11)

        
        # Colors for different delivery trucks
        colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'darkblue']
        
        for v_id, route in enumerate(routes):
            route_coords = []
            route_weight = 0
            
            for node_index in route:
                lat = logistics_df.iloc[node_index]['Latitude']
                lon = logistics_df.iloc[node_index]['Longitude']
                route_coords.append([lat, lon])
                route_weight += demands[node_index]
                
                # Draw delivery markers (skipping the Hub itself)
                if node_index != 0:
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=5,
                        popup=f"Order {node_index} | Weight: {demands[node_index]}kg",
                        color=colors[v_id % len(colors)],
                        fill=True
                    ).add_to(m)
                    
            # Draw the actual path line for the truck
            folium.PolyLine(
                route_coords,
                color=colors[v_id % len(colors)],
                weight=4,
                opacity=0.8,
                popup=f"Vehicle {v_id+1} Route (Total Load: {route_weight}kg)"
            ).add_to(m)
            
        # Render the map in Streamlit
        folium_static(m)
        
    else:
        st.error("❌ No solution found! The trucks might not have enough capacity for all these packages. Try adding more vehicles or increasing capacity.")