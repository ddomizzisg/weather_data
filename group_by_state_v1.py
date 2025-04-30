from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import glob
import pandas as pd

# Path to your CSV files (adjust the pattern as needed)
csv_files = glob.glob('data/*.csv')

df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Get unique stations and coordinates
stations = df[['STATION', 'LATITUDE', 'LONGITUDE']].drop_duplicates()

# Initialize geolocator
geolocator = Nominatim(user_agent="mexico_station_locator")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

# Reverse geocode to get state
def get_state(lat, lon):
    try:
        location = geocode((lat, lon), exactly_one=True, language='en')
        print(location)
        return location.raw['address'].get('state')
    except:
        return None

stations['STATE'] = stations.apply(lambda row: get_state(row['LATITUDE'], row['LONGITUDE']), axis=1)

# Merge back into the main dataframe
df = df.merge(stations[['STATION', 'STATE']], on='STATION', how='left')

# Save the updated dataframe with state information
df.to_csv('data/gsod_with_states.csv', index=False)