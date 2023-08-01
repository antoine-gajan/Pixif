from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy import Nominatim
import subprocess
import directories_manangement as dm

def open_image(picture_path : str):
    """Opens an image from a path and returns a PIL Image object."""
    return Image.open(picture_path)

def picture_exif_data(picture_path : str):
    """Returns a dictionary from the exif data of an PIL Image."""
    exif_data = {}
    img = open_image(picture_path)
    # Get the exif data
    info = img._getexif()
    if info:
        # Iterate over all tags and extract the GPS tags
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            # If the tag is GPSInfo, parse it
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            # If the tag is not GPSInfo, convert it to string
            else:
                exif_data[decoded] = value
    # Return the exif data
    return exif_data

def video_exif_data(video_path : str):
    """Returns a dictionary from the exif data of a video."""
    exif_data = {}
    exif_data["GPSInfo"] = {}
    # Write the complete path of the ExifTool in your device along with .exe at last
    exe = "exiftool.exe_PATH"
    # Execute the ExifTool command
    process = subprocess.Popen([exe, video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    # For each metadata
    for output in process.stdout:
        # Split the output at the first colon
        key, val = output.strip().split(":", 1)
        # Remove the whitespace from the key and value
        key = key.strip()
        val = val.strip()
        # If the key contains "GPS"
        if "GPS" in key:
            # If the key is GPS Latitude or Longitude
            if key == "GPS Latitude" or key == "GPS Longitude":
                # Get the position from the string value
                position = string2position(val)
                # If the key is GPS Latitude
                if key == "GPS Latitude":
                    # Add the latitude to the dictionary
                    exif_data["GPSInfo"]["GPSLatitude"] = position[0]
                    # Add the latitude reference to the dictionary
                    exif_data["GPSInfo"]["GPSLatitudeRef"] = position[1]
                # If the key is GPS Longitude
                else:
                    # Add the longitude to the dictionary
                    exif_data["GPSInfo"]["GPSLongitude"] = position[0]
                    # Add the longitude reference to the dictionary
                    exif_data["GPSInfo"]["GPSLongitudeRef"] = position[1]
        else:
            # Add the key and value to the dictionary
            exif_data[key] = val
    # Return the exif data
    return exif_data

def string2position(position : str) -> tuple:
    """Converts a string position from ExifTool to a tuple of float."""
    # Split the string with a whitespace
    position = position.split(" ")
    # Remove the second element of the position
    position.pop(1)
    # Remove the last character of the second and third element
    position[1] = position[1][:-1]
    position[2] = position[2][:-1]
    # Get ref and position
    ref = position.pop(3)
    position = [float(p) for p in position]
    # Convert position to a tuple of float
    position = tuple(position)  # (degrees, minutes, seconds)
    return position, ref


def exif2decimal_position(GPSInfo : dict) -> tuple:
    """Converts the GPSInfo from get_exif_data() to a decimal position."""
    # Get the information from the GPSInfo dictionary
    lat = GPSInfo["GPSLatitude"]
    lat_ref = GPSInfo["GPSLatitudeRef"]
    lon = GPSInfo["GPSLongitude"]
    lon_ref = GPSInfo["GPSLongitudeRef"]
    # Compute lat and long decimal values
    lat = (lat[0] + lat[1]/60 + lat[2]/3600) * (-1 if lat_ref == "S" else 1)
    lon = (lon[0] + lon[1]/60 + lon[2]/3600) * (-1 if lon_ref == "W" else 1)
    return (lat, lon)

def get_location(lat : float, lon : float):
    """Returns the location of the given coordinates."""
    geolocator = Nominatim(user_agent="SortHolidaysPicture")
    location = geolocator.reverse((lat, lon))
    return location.raw["address"]

def place(location : dict) -> str:
    """Returns the place of the given location."""
    if "tourism" in location:
        return dm.correct_place(location["tourism"])
    if "city" in location:
        return dm.correct_place(location["city"])
    if "village" in location:
        return dm.correct_place(location["village"])
    if "town" in location:
        return dm.correct_place(location["town"])
    if "country" in location:
        return dm.correct_place(location["country"])

def is_place_corresponding(location : dict, place_expected : str, exact_match : bool) -> bool :
    """Return True is the place expected is correct"""
    place_expected = dm.correct_place(place_expected)
    # For each element in the location
    for element, value in location.items():
        correct_value = dm.correct_place(value)
        if exact_match and correct_value == place_expected:
            return True
        elif not exact_match and place_expected in correct_value:
            return True
    return False



def get_date_from_exif(exif_data : dict) -> str:
    """Returns the date of the picture based on exif_data."""
    # For picture data
    if "DateTimeOriginal" in exif_data:
        return exif_data["DateTimeOriginal"].split(" ")[0]
    elif "DateTimeDigitized" in exif_data:
        return exif_data["DateTimeDigitized"].split(" ")[0]
    # For video data
    elif "File Modification Date/Time" in exif_data:
        return exif_data["File Modification Date/Time"].split(" ")[0]
    else:
        return "Unknown"

def date(exif : dict) -> str:
    """Returns the date of the picture based on exif data."""
    date = get_date_from_exif(exif)
    if date != "Unknown":
        return "-".join(date.split(":"))
