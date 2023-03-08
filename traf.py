import folium


m = folium.Map(location=[32.0926596, 34.7746982])
tooltip = "Click me!"

folium.Marker(
    [32.0926596, 34.7746982],
    popup="<i>Mt. Hood Meadows</i>",
    icon=folium.Icon(icon="cloud")
).add_to(m)
folium.Marker(
    [32.0826596, 34.8746982],
    popup="<b>Timberline Lodge</b>",
    icon=folium.Icon(color="red", icon="info-sign"),

).add_to(m)

folium.Marker(
    [32.2708,  34.8445],
    popup="<i>Alon Reicher's house</i>",
    icon=folium.Icon(icon="sun-o", prefix="fa")
).add_to(m)
m.add_child(folium.LatLngPopup())
m.add_child(folium.ClickForMarker(popup="Waypoint"))


m
m.save("index.html")
