import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import haversine_distances, pairwise_distances

# Load data
df = pd.read_csv("with_states.csv")
df = df[['STATION', 'TEMP', 'PRCP', 'LATITUDE', 'LONGITUDE']].dropna()
df = df.groupby('STATION').agg({
    'TEMP': 'mean',
    'PRCP': 'mean',
    'LATITUDE': 'mean',
    'LONGITUDE': 'mean'
}).reset_index()

# Normalize climate features
scaler = StandardScaler()
climate_scaled = scaler.fit_transform(df[['TEMP', 'PRCP']])

# Haversine distance (in radians → km)
coords_rad = np.radians(df[['LATITUDE', 'LONGITUDE']])
geo_dist = haversine_distances(coords_rad) * 6371  # in km
geo_dist_norm = geo_dist / geo_dist.max()

# Combine climate + geo distances
climate_dist = pairwise_distances(climate_scaled)
combined_dist = 0.7 * climate_dist + 0.3 * geo_dist_norm

# k-distance plot: distance to the 4th nearest neighbor (min_samples - 1)
min_samples = 5
nbrs = NearestNeighbors(n_neighbors=min_samples, metric='precomputed').fit(combined_dist)
distances, indices = nbrs.kneighbors(combined_dist)

# Sort and plot distances
k_distances = np.sort(distances[:, -1])  # distances to k-th neighbor
plt.figure(figsize=(8, 4))
plt.plot(k_distances)
plt.xlabel("Points sorted by distance")
plt.ylabel(f"Distance to {min_samples}th nearest neighbor")
plt.title("DBSCAN eps selection (elbow method)")
plt.grid(True)
plt.tight_layout()
plt.savefig("dbscan_elbow.png")
plt.show()
