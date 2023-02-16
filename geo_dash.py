import dash
#from dash import Dash, html, dcc
import dash_html_components as html
import exifread
import os
import requests

import plotly.express as px

app = dash.Dash(__name__)

def extract_gps_info(photo_path):
    with open(photo_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)

        lat_deg = tags.get('GPS GPSLatitude', None)
        lat_ref = tags.get('GPS GPSLatitudeRef', None)
        long_deg = tags.get('GPS GPSLongitude', None)
        long_ref = tags.get('GPS GPSLongitudeRef', None)
        timestamp = tags.get('EXIF DateTimeOriginal', None)

        if lat_deg and lat_ref and long_deg and long_ref:
            latitude = convert_to_degrees(lat_deg, lat_ref)
            longitude = convert_to_degrees(long_deg, long_ref)
            return (latitude, longitude, timestamp)
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


CURR_DIR_PATH = os.getcwd()
photo_path = CURR_DIR_PATH + "//data//seg_our//seg_our//live.jpg"
#photo_path = CURR_DIR_PATH + '/cinisi.jpg'
location = extract_gps_info(photo_path)

#figure = px.imshow(photo_path)
#style={'width': '50%', 'height': 'auto'}
print(photo_path)

if location:
    location_name, country = get_location_name(location[0], location[1])

    app.layout = html.Div([
        html.H3("Geolocation information for image"),
        html.P("Timestamp: {}".format(location[2])),
        html.P("Latitude: {:.6f}°".format(location[0])),
        html.P("Longitude: {:.6f}°".format(location[1])),
        html.P("Country: {}".format(country)),
        html.P("Location Name: {}".format(location_name)),

        html.Div(children=[
            html.Img(src='assets/live.jpg', style={'width': '100px', 'height': '100px'})
        ], style={'align':'center'})
    ])


else:
    app.layout = html.Div([
        #html.H3("No Geolocation Information Found in Photo"),
        

        
    ])

if __name__ == '__main__':
    app.run_server()
