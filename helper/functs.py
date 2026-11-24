import os
from pathlib import Path
import json
import pandas as pd

def get_my_www_folder() -> Path:
    """This function returns the path to the 'www' folder, 
    which is located in the parent directory of the current file's directory.
    Returns:
        Path: www folder path
    """
    return Path(__file__).resolve().parents[1] / 'www'

def phs_config_get(file_path: str) -> dict:
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

def get_social_urls(cfg: dict) -> dict:
    """Extract social media URLs from a JSON dictionary.
    Args:
        json (dict): The input JSON dictionary containing social media information.
    Returns:
        dict: A dictionary containing the extracted social media URLs.
    """
    if cfg.get("footer") is None:
        return {}
    social = cfg.get("footer").get("social_media", {})
    social_elements = social.get("links", {})
    return social_elements

def get_phs_url(cfg: dict) -> str:
    """Extract the URL from a JSON dictionary.
    Args:
        json (dict): The input JSON dictionary containing the URL information.
    Returns:
        str: The extracted URL.
    """
    if cfg.get("footer") is None:
        return ""
    return cfg.get("footer").get("publichealthscotland_url", "")

def get_ogl_url(cfg: dict) -> str:
    """Extract the OGL URL from a JSON dictionary.
    Args:
        json (dict): The input JSON dictionary containing the OGL URL information.
    Returns:
        str: The extracted OGL URL.
    """
    if cfg.get("footer") is None:
        return ""
    return cfg.get("footer").get("ogl_license_url", "")

def get_compliance_list(cfg: dict) -> dict:
    """Extract the compliance information from a JSON dictionary.
    Args:
        json (dict): The input JSON dictionary containing the compliance information.
    Returns:
        dict: The extracted compliance information.
    """
    if cfg.get("compliance") is None:
        return {}
    return cfg.get("compliance", {})

def build_data_context(data: pd.DataFrame) -> str:
    cols_info = "\n".join(
        f"- {col!r} ({data[col].dtype}): "
        f"non-null={data[col].notna().sum()}/{len(data)}"
        for col in data.columns
    )
    numeric_columns = data.select_dtypes(include="number")
    numeric_summary = (
        numeric_columns.describe().to_string()
        if len(numeric_columns.columns) > 0
        else "No numeric columns."
    )
    return (
        f"Dataset has {len(data)} rows and {len(data.columns)} columns.\n"
        f"Columns and types:\n{cols_info}\n\n"
        f"Numeric summary:\n{numeric_summary}"
    )
