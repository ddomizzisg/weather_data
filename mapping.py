import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import argparse

class Mapping:

    def __init__(self, stations):
        self.stations = stations

    def plot(self, shape_file="states.geojson",  output_path="station_clusters_map.png"):
        # Create geometry for each station
        geometry = [Point(xy) for xy in zip(self.stations['LONGITUDE'], self.stations['LATITUDE'])]
        stations_gdf = gpd.GeoDataFrame(self.stations, geometry=geometry, crs="EPSG:4326")

        # Load map of Mexican states
        states_gdf = gpd.read_file(shape_file)

        # Plot
        fig, ax = plt.subplots(figsize=(12, 10))
        states_gdf.plot(ax=ax, color='whitesmoke', edgecolor='gray')
        stations_gdf.plot(ax=ax, column='CLUSTER', cmap='Set2', legend=True, markersize=40, alpha=0.8)

        plt.title("Weather Stations Clustered by Temperature & Precipitation")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forecast temperature for a specific station.")
    parser.add_argument("csv_path", type=str, help="Path to the CSV file.")
    parser.add_argument("--shape_file", default="states.geojson", type=str, help="Path to the shapefile.")
    parser.add_argument("--output_path", default="map.png", type=str, help="Path to the output image.")
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.csv_path)

    map = Mapping(df)
    map.plot(shape_file=args.shape_file, output_path=args.output_path)
    print(f"Map saved to {args.output_path}")