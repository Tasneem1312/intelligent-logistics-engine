import pandas as pd
import numpy as np

def generate_logistics_data(num_orders, hub_lat, hub_lon, radius_km):
    """
    Generates synthetic delivery data around a central hub.
    """
    # 1 degree of latitude is approximately 111 km
    # We use this to convert our km radius into a coordinate offset
    radius_in_degrees = radius_km / 111.0 
    
    orders = []
    
    for i in range(1, num_orders + 1):
        # Generate random offsets for latitude and longitude within the radius
        # The np.random.uniform creates a random spread of locations
        u = np.random.uniform(0, 1)
        v = np.random.uniform(0, 1)
        
        w = radius_in_degrees * np.sqrt(u)
        t = 2 * np.pi * v
        
        # Calculate final coordinates for the delivery point
        order_lat = hub_lat + w * np.cos(t)
        order_lon = hub_lon + w * np.sin(t)
        
        # Assign a random package weight between 1kg and 25kg
        weight = np.random.randint(1, 26)
        
        orders.append({
            'Order_ID': f'ORD_{i:03d}',
            'Latitude': order_lat,
            'Longitude': order_lon,
            'Delivery_Weight_kg': weight
        })
        
    return pd.DataFrame(orders)

# Central Warehouse coordinates (Vellore)
HUB_LAT = 12.9165
HUB_LON = 79.1325

# Generate 50 unique orders within a 15km radius of the hub
df_orders = generate_logistics_data(num_orders=50, hub_lat=HUB_LAT, hub_lon=HUB_LON, radius_km=15)

# Add the Hub itself as the starting point (Order_ID: HUB) with 0 weight
hub_data = pd.DataFrame([{
    'Order_ID': 'HUB', 
    'Latitude': HUB_LAT, 
    'Longitude': HUB_LON, 
    'Delivery_Weight_kg': 0
}])

# Combine the hub and the orders into one dataset
logistics_df = pd.concat([hub_data, df_orders], ignore_index=True)

print(logistics_df.head())