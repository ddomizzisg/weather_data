import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv("with_states.csv")  # Adjust path if needed

# Ensure numeric types
for col in ['TEMP', 'PRCP', 'ELEVATION', 'LATITUDE', 'LONGITUDE']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing values
df = df.dropna(subset=['TEMP', 'PRCP', 'ELEVATION', 'LATITUDE', 'LONGITUDE'])

# Compute average stats per station
station_stats = df.groupby('STATION')[['TEMP', 'PRCP', 'ELEVATION', 'LATITUDE', 'LONGITUDE']].mean().reset_index()

# Standardize features
features = ['TEMP', 'PRCP', 'ELEVATION', 'LATITUDE', 'LONGITUDE', 'SLP']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(station_stats[features])

# Run KMeans clustering
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
station_stats['CLUSTER'] = kmeans.fit_predict(X_scaled)

# Plot cluster centers in TEMP–PRCP space (for visualization)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=station_stats, x='TEMP', y='PRCP', hue='CLUSTER', palette='Set2', s=100)
plt.title("Station Clusters (TEMP vs PRCP)")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Average Precipitation")
plt.legend(title="Cluster")
plt.tight_layout()
plt.savefig("cluster_extended.png")
#plt.show()

# Save results
station_stats.to_csv("clustered_stations_extended.csv", index=False)