import os
import json
from datetime import datetime

def create_folder_if_not_exists():
    """Creates the app/logs directory if it doesn't exist.

    returns:
    log_path (str): Path of the app/logs directory, either already or newly created.
    """

    # Get directory of this file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get parent directory
    parent_dir = os.path.dirname(script_dir)
    # Define path for log folder
    log_path = os.path.join(parent_dir, 'logs')

    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    return log_path

def store_debug_log(object: dict):
    """ Takes a serializable dictionary and stores it as a json in the app/logs/ directory.

    args:
    object (dict): Object to be stored

    returns:
    path (str): Path of the object

    """

    path = create_folder_if_not_exists()

    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debug_log_{timestamp}.json"
    
    # Create full file path
    file_path = os.path.join(path, filename)
    
    # Write json to file
    with open(file_path, 'w') as f:
        json.dump(object, f, indent=2)
        
    return file_path