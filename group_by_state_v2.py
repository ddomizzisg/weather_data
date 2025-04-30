from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import glob
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# Path to your CSV files (adjust the pattern as needed)
csv_files = glob.glob('data/*.csv')

df = pd.concat([pd.read_csv(f, low_memory=False) for f in csv_files], ignore_index=True)

# Get unique stations and coordinates
stations = df[['STATION', 'LATITUDE', 'LONGITUDE']].drop_duplicates()

# Convert your station coordinates into a GeoDataFrame
geometry = [Point(xy) for xy in zip(df['LONGITUDE'], df['LATITUDE'])]
stations_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Drop conflicting column if it exists
if 'index_right' in stations_gdf.columns:
    stations_gdf = stations_gdf.drop(columns='index_right')

# Load Mexican states shapefile or GeoJSON
states_gdf = gpd.read_file("states.geojson")
states_subset = states_gdf[['geometry', 'state_name', 'state_code']]

# Spatial join
stations_with_state = gpd.sjoin(stations_gdf, states_subset, how="left", predicate="within")
stations_with_state = stations_with_state.rename(columns={'state_name': 'STATE', 'state_code': 'STATE_CODE'})


stations_with_state = stations_with_state.drop(columns=['geometry', 'index_right'], errors='ignore')

# Also remove duplicate or redundant columns if needed
stations_with_state = stations_with_state.loc[:, ~stations_with_state.columns.duplicated()]

#Convert code column to integer
stations_with_state['STATE_CODE'] = stations_with_state['STATE_CODE'].astype('Int64')

print(stations_with_state.head())

# Save the updated dataframe with state information
stations_with_state.to_csv('with_states.csv', index=False)