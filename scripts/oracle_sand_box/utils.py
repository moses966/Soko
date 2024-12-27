import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = f"../deployments.json"

def edit_value(_key, _value):
    file_path = os.path.join(base_dir, relative_path)
    with open(file_path, "r+") as file:  # Use 'r+' mode to read and write in one go
        data = json.load(file)
        data[_key] = _value
        file.seek(0)  # Move to the start of the file for writing
        json.dump(data, file, indent=4)
        file.truncate()  # Remove any leftover data from previous content if shorter
    # Ensure data is on disk
    with open(file_path, "rb") as f:  # Open in binary mode for os.fsync
        os.fsync(f.fileno())

def get_value(_key):
    file_path = os.path.join(base_dir, relative_path)
    # Small delay to ensure file system has updated
    with open(file_path, "r") as file:
        data = json.load(file)
    
    return data[_key]