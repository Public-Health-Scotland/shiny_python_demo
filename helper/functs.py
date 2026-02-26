from datetime import datetime
import os
from pathlib import Path
import json

def read_my_json(file_path: str) -> dict:
    """Read a JSON file and return its contents as a dictionary.
    Args:
        file_path (str): The path to the JSON file.
    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    if not os.path.exists(file_path):
        return {}
    data = json.loads(Path(file_path).read_text())
    return data
