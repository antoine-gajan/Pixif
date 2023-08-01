import webbrowser

import folium

def create_map():
    """Create the map"""
    map = folium.Map(zoom_start=1)
    return map

def add_marker(map, lat, lon, img):
    """Add a marker to the map"""
    # Add a marker with a custom icon and popup
    icon = folium.features.CustomIcon(img, icon_size=(50, 50))
    marker = folium.Marker(location=[lat, lon], icon=icon)
    marker.add_to(map)
    img = img.replace("\\","/")
    popup = folium.Popup(f'<img src="{img}" alt="Image" style="max-width:200px">', max_width=250)
    marker.add_child(popup)
    # Return the updated map
    return map


def save_map(map):
    """Save the map"""
    map.save("map.html")

def web_view(file : str):
    """Open the map in a web browser"""
    webbrowser.open(file)

