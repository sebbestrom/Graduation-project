import exifread
import os
import requests

def extract_gps_info(photo_path):
    with open(photo_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)

        lat_deg = tags.get('GPS GPSLatitude', None)
        lat_ref = tags.get('GPS GPSLatitudeRef', None)
        long_deg = tags.get('GPS GPSLongitude', None)
        long_ref = tags.get('GPS GPSLongitudeRef', None)

        if lat_deg and lat_ref and long_deg and long_ref:
            latitude = convert_to_degrees(lat_deg, lat_ref)
            longitude = convert_to_degrees(long_deg, long_ref)
            return (latitude, longitude)
        else:
            return None

def convert_to_degrees(coordinate, ref):
    coordinate = list(coordinate.values)
    d = float(coordinate[0].num) / coordinate[0].den
    m = float(coordinate[1].num) / coordinate[1].den
    s = float(coordinate[2].num) / coordinate[2].den
    result = d + (m / 60.0) + (s / 3600.0)
    if ref == 'S' or ref == 'W':
        result *= -1
    return result

def get_location_name(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    location_name = response.json().get('address').get('town') or response.json().get('address').get('city')
    country = response.json().get('address').get('country')
    return location_name, country

# Example Usage:
CURR_DIR_PATH = os.getcwd()
photo_path = CURR_DIR_PATH + '/gdansk.jpg'
location = extract_gps_info(photo_path)
if location:
    print("\nThe geolocation information for the photo:")
    print("Latitude: {:.6f}°".format(location[0]))
    print("Longitude: {:.6f}°".format(location[1]))
    location_name, country = get_location_name(location[0], location[1])
    print("Country:", country)
    print("Location name:", location_name)
    
else:
    print("\nNo geolocation information found in the photo.")
