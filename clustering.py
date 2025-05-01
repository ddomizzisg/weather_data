import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

class KMeansStationsCluster(object):

    def __init__(self, df, features, n_clusters=4, output="clustered_stations.csv", year=None):
        self.df = df
        self.features = features
        self.output = output
        self.n_clusters = n_clusters
        self.year = year

    def run(self):

        # Ensure 'DATE' is datetime
        self.df['DATE'] = pd.to_datetime(self.df['DATE'], errors='coerce')

        # Extract year and convert temperature to numeric
        self.df['YEAR'] = self.df['DATE'].dt.year

        if self.year is not None:
            # Filter the dataframe for the specified year
            self.df = self.df[self.df['YEAR'] == self.year]

        # Compute average stats per station
        station_stats = self.df.groupby('STATION')[self.features].mean().reset_index()

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(station_stats[self.features])

        # Run KMeans clustering
        n_clusters = 4
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        station_stats['CLUSTER'] = kmeans.fit_predict(X_scaled)

        self.stations_with_clusters = station_stats

        return self.stations_with_clusters
    
    def plot_clusters(self, output_path="cluster_plot.png"):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.stations_with_clusters, x='TEMP', y='PRCP', hue='CLUSTER', palette='Set2', s=100)
        plt.title("Station Clusters (TEMP vs PRCP)")
        plt.xlabel("Average Temperature (°C)")
        plt.ylabel("Average Precipitation")
        plt.legend(title="Cluster")
        plt.tight_layout()
        plt.savefig(output_path)
        
    
    def save_results(self):
        self.stations_with_clusters.to_csv(self.output, index=False)
        print(f"Clustered stations saved to {self.output}")
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cluster weather stations using KMeans.")
    parser.add_argument("csv_path", type=str, help="Path to the CSV file.")
    parser.add_argument("--features", nargs='+', default=['TEMP', 'PRCP', 'ELEVATION', 'LATITUDE', 'LONGITUDE'], help="Features for clustering.")
    parser.add_argument("--n_clusters", type=int, default=4, help="Number of clusters.")
    parser.add_argument("--year", type=int, help="Year to filter data.")
    args = parser.parse_args()

    df = pd.read_csv(args.csv_path)
    
    clus = KMeansStationsCluster(df, args.features, n_clusters=args.n_clusters, year=args.year)
    clus.run()
    clus.plot_clusters()
    clus.save_results()
