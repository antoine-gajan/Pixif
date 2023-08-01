import os
import shutil
import re

def create_subdirectory(directory : str, subdirectory : str) -> str:
    """Creates a subdirectory in the given directory if it doesn't exist."""
    # Create the full path for the subdirectory
    subdirectory_path = os.path.join(directory, subdirectory)
    # Check if the subdirectory already exists
    if not os.path.exists(subdirectory_path):
        # Create the subdirectory if it doesn't exist
        os.makedirs(subdirectory_path)
        print(f"Subdirectory '{subdirectory}' created successfully.")
    else:
        print(f"Subdirectory '{subdirectory}' already exists.")
    return subdirectory_path


def move_file(file : str, destination : str) -> str:
    """Moves the file to the destination."""
    # Move the file to the destination directory
    try:
        shutil.move(file, destination)
        print(f"File '{file}' moved successfully.")
        return os.path.join(destination, file)
    except Exception as e:
        print(f"Error moving file: {e}")

def number_of_files(directory : str) -> int:
    """Returns the number of files in the given directory."""
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return len(files)

def number_of_images_or_videos(directory : str) -> int:
    """Returns the number of images or videos in the given directory."""
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)) and (is_image(file) or is_video(file))]
    return len(files)

def is_image(path : str) -> bool:
    """Returns True if the file at the given path is an image."""
    return path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))

def is_video(path : str) -> bool:
    """Returns True if the file at the given path is a video."""
    return path.lower().endswith((".mp4", ".avi", ".mov"))

def is_directory(path : str) -> bool:
    """Returns True if the file at the given path is a directory."""
    return os.path.isdir(path)

def string2camel_case(string : str) -> str:
    """Converts a string to camel case."""
    return ''.join(x for x in string.title() if x.isalpha())

def correct_place(string : str) -> str:
    # Keep only letters, spaces, numbers
    string = re.sub(r"[^a-zA-Z0-9 \-]+", "", string)
    return string2camel_case(string)
