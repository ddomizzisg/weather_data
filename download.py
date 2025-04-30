import requests
from bs4 import BeautifulSoup
import os

output_dir = "gsod_data"
os.makedirs(output_dir, exist_ok=True)

base_url = f"https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/"

# Get the list of files
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    filename = link.get('href')
    year_url = base_url + filename
    print(f"Downloading {year_url}...")
    year_out_dir = os.path.join(output_dir, filename)

    if year_out_dir.startswith("/data"): 
        continue

    print(year_out_dir)
    os.makedirs(year_out_dir, exist_ok=True)

    # # Get the list of files
    response = requests.get(year_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for link in soup.find_all('a'):
        filename = link.get('href')
        if filename.endswith(".csv"):
            file_url = year_url + filename
            print(f"Downloading {year_url}...")
            file_data = requests.get(file_url).content
            with open(os.path.join(year_out_dir, filename), 'wb') as f:
                f.write(file_data)




# year = "2023"
# base_url = f"https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/"



# # Get the list of files
# response = requests.get(base_url)
# soup = BeautifulSoup(response.text, 'html.parser')

# for link in soup.find_all('a'):
#     filename = link.get('href')
#     if filename.endswith(".csv"):
#         file_url = base_url + filename
#         
#         file_data = requests.get(file_url).content
#         with open(os.path.join(output_dir, filename), 'wb') as f:
#             f.write(file_data)
