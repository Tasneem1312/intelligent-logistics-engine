import numpy as np
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points 
    on the Earth's surface in kilometers.
    """
    R = 6371.0  # Earth's radius in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

def create_distance_matrix(df):
    """
    Generates a 2D distance matrix for all nodes in the dataframe.
    Matrix[i][j] represents the distance from node i to node j.
    """
    num_nodes = len(df)
    
    # Initialize an empty matrix with zeros
    matrix = np.zeros((num_nodes, num_nodes))
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:  # Distance to itself is 0
                matrix[i][j] = haversine_distance(
                    df.iloc[i]['Latitude'], df.iloc[i]['Longitude'],
                    df.iloc[j]['Latitude'], df.iloc[j]['Longitude']
                )
                
    return matrix

if __name__ == "__main__":
    # Mock data to test the function
    mock_data = pd.DataFrame({
        'Latitude': [12.9165, 12.9200, 12.9100],
        'Longitude': [79.1325, 79.1400, 79.1300]
    })
    
    dist_matrix = create_distance_matrix(mock_data)
    print("Distance Matrix (in km):")
    print(np.round(dist_matrix, 2))