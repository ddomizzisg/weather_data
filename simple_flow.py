from forecasting import WeatherForecast
from clustering import KMeansStationsCluster
from regressions import StationsLinearRegression
from mapping import Mapping
import os

import argparse
import pandas as pd

dataset_path = "with_states.csv"
N_CLUSTERS = 3

# Load data
df = pd.read_csv(dataset_path)

# clustering
features = ['TEMP', 'PRCP', 'ELEVATION', 'LATITUDE', 'LONGITUDE']
clus = KMeansStationsCluster(df, features, n_clusters=N_CLUSTERS)
clus.run()
clus.plot_clusters()
clus.save_results()

# mapping (Clustering --> Mapping)
map = Mapping(clus.stations_with_clusters)
map.plot(shape_file="states.geojson", output_path="station_clusters_map.png")
print("Map saved to station_clusters_map.png")

# regression (Clustering --> Regression)
stations_clustered = clus.stations_with_clusters

for i in range(N_CLUSTERS):
    stations = stations_clustered[stations_clustered['CLUSTER'] == i]
    stations = stations.reset_index(drop=True)
    print(f"Running regression for cluster {i} with {len(stations)} stations")
    
    # Create a new dataframe from df only with stations in the cluster
    df_cluster = df[df['STATION'].isin(stations['STATION'])]
    df_cluster = df_cluster.reset_index(drop=True)

    # Make some modifications to the dataframe

    # Ensure 'DATE' is datetime
    df_cluster['DATE'] = pd.to_datetime(df_cluster['DATE'], errors='coerce')
    # Extract year and convert temperature to numeric
    df_cluster['YEAR'] = df_cluster['DATE'].dt.year
    df_cluster['TEMP'] = pd.to_numeric(df_cluster['TEMP'], errors='coerce')

    # Convert from Fahrenheit to Celsius
    df_cluster['TEMP'] = (df_cluster['TEMP'] - 32) * 5 / 9

    # Drop rows with missing years or temperatures
    df_cluster = df_cluster.dropna(subset=['YEAR', 'TEMP'])

    # Group by year and compute average temperature
    avg_temp_per_year = df_cluster.groupby('YEAR')['TEMP'].mean().reset_index()

    # Remove year 2025
    avg_temp_per_year = avg_temp_per_year[avg_temp_per_year['YEAR'] != 2025]


    # Perform regression
    reg = StationsLinearRegression(avg_temp_per_year, 'YEAR', 'TEMP')
    reg.fit()
    reg.plot(output=f"regression_results_cluster_{i}.png")
    print(f"Regression results for cluster {i} saved to regression_results_cluster_{i}.png")

# Forecasting per station
stations = df['STATION'].unique()

wf = WeatherForecast(df)
for station in stations:
    os.makedirs("results", exist_ok=True)
    wf.fit(station, column_station_name="STATION", date_column="DATE", temp_column="TEMP")
    forecast = wf.forecast(days=100)
    wf.plot(forecast, station, output_prefix="results/forecast")