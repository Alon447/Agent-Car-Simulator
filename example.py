import folium

# Create a map using OSM tiles
map = folium.Map(location=[40.7128, -74.0060], zoom_start=12, tiles='OpenStreetMap')

# Add a marker to the map
marker = folium.Marker(location=[40.7128, -74.0060], popup="New York City")
marker.add_to(map)

# Display the map
map