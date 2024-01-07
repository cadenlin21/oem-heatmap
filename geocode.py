import pandas as pd
from geopy.geocoders import Nominatim
import time

# Initialize the Geolocator
geolocator = Nominatim(user_agent="your_app_name")

def get_coordinates(location):
    try:
        location = geolocator.geocode(location)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error occurred for location '{location}': {str(e)}")
        return None, None

# List of locations (replace with your locations)
with open('locations.txt', 'r') as file:
    locations = [line.strip() for line in file]

# Prepare a list to hold the geocoded data
data = []

# Geocode each location
for place in locations:
    lat, lon = get_coordinates(place)
    print(place, lat, lon)
    data.append({"name": place, "lat": lat, "lon": lon})
    time.sleep(1)  # To comply with rate limiting

# Create a DataFrame
df = pd.DataFrame(data)

# Export to Excel
df.to_excel("geocoded_locations.xlsx", index=False)

print("Excel file created successfully.")

