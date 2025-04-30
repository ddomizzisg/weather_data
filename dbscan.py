import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import haversine_distances
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
df = pd.read_csv("with_states.csv")
df['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce')
df['PRCP'] = pd.to_numeric(df['PRCP'], errors='coerce')
df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')

df = df.dropna(subset=['TEMP', 'PRCP', 'LATITUDE', 'LONGITUDE'])

# Aggregate data by station
station_stats = df.groupby('STATION').agg({
    'TEMP': 'mean',
    'PRCP': 'mean',
    'LATITUDE': 'mean',
    'LONGITUDE': 'mean'
}).reset_index()

# Step 1: Normalize non-geospatial features
scaler = StandardScaler()
climate_features = scaler.fit_transform(station_stats[['TEMP', 'PRCP']])

# Step 2: Convert lat/lon to radians for Haversine
coords_rad = np.radians(station_stats[['LATITUDE', 'LONGITUDE']].to_numpy())

# Step 3: Compute Haversine distances (in radians)
geo_dist = haversine_distances(coords_rad)  # returns radians

# Optional: scale to km (Earth radius ~6371 km)
geo_dist_km = geo_dist * 6371

# Step 4: Combine climate + geographic similarity
# We'll define a composite distance: 80% climate, 20% geo
from sklearn.metrics import pairwise_distances

climate_dist = pairwise_distances(climate_features)
combined_dist = 0.99 * climate_dist + 0.01 * (geo_dist_km / geo_dist_km.max())  # normalize geo_dist

# Step 5: Run DBSCAN on custom distance matrix
db = DBSCAN(eps=0.5, min_samples=4, metric='precomputed')
station_stats['CLUSTER'] = db.fit_predict(combined_dist)

# Step 6: Plot results
plt.figure(figsize=(10, 6))
sns.scatterplot(data=station_stats, x='LONGITUDE', y='LATITUDE',
                hue='CLUSTER', palette='tab10', s=100)
plt.title("Weather Station Clusters (DBSCAN + Climate + Location)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(title="Cluster")
plt.tight_layout()
plt.savefig("dbscan_clusters.png")
plt.show()

# Save results
station_stats.to_csv("dbscan_clustered_stations.csv", index=False)
