import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load clustered station data
stations = pd.read_csv("clustered_stations.csv")

# Load original dataset to get coordinates
raw_data = pd.read_csv("with_states.csv")
coords = raw_data[['STATION', 'LATITUDE', 'LONGITUDE']].drop_duplicates()

# Merge to get lat/lon into the clustered data
stations = stations.merge(coords, on='STATION', how='left')

# Drop rows without coordinates
stations = stations.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Create geometry for each station
geometry = [Point(xy) for xy in zip(stations['LONGITUDE'], stations['LATITUDE'])]
stations_gdf = gpd.GeoDataFrame(stations, geometry=geometry, crs="EPSG:4326")

# Load map of Mexican states
states_gdf = gpd.read_file("states.geojson")

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
states_gdf.plot(ax=ax, color='whitesmoke', edgecolor='gray')
stations_gdf.plot(ax=ax, column='CLUSTER', cmap='Set2', legend=True, markersize=40, alpha=0.8)

plt.title("Weather Stations Clustered by Temperature & Precipitation")
plt.axis("off")
plt.tight_layout()
plt.savefig("station_clusters_map.png")
