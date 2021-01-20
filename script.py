# Importing themodule
from folium import *
import pandas

# Extracting the data
data = pandas.read_csv("Volcanoes.csv")
lat = list(data["Latitude (dd)"])
lon = list(data["Longitude (dd)"])
elev = list(data["Elevation (m)"])
name = list(data["Volcano Name"])
country = list(data["Country"])

# Functions
# Giving out the colours


def colour_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


# creating the popup
html = """
    Volcano name:<br>
    <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank" style="text-decoration: none;">%s</a><br>
    Height: %s m<br>
    Country: %s
    """

# Creating the map
map = Map(location=[0, 0],
          zoom_start=4, tiles="Stamen Terrain", min_zoom=2)
# Creating the feature groups
fgv = FeatureGroup(name="Volcanoes")
fgp = FeatureGroup(name="Population")

# Adding the markers
for lt, ln, el, name, place in zip(lat, lon, elev, name, country):
    iframe = IFrame(html=html % (
        name, name, el, place), width=200, height=100)
    fgv.add_child(CircleMarker(location=[lt, ln], radius=8, popup=Popup(
        iframe), fill_color=colour_producer(el), color="grey", fill_opacity=0.7))

# Adding the population layer
fgp.add_child(GeoJson(data=open('world.json', 'r',
                                encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000 <= x['properties']['POP2005'] < 20000000 else 'red'})).add_child(Popup("Hi"))
# Adding the feature group
map.add_child(fgp)
map.add_child(fgv)

# Adding the layer controller
map.add_child(LayerControl())

# Saving to the HTML file
map.save("index.html")
