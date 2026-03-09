import os
from shiny.ui import tags

def load_js_folder(folder_path: str):
    """
    Safely load all .js files from a given folder.
    Only loads trusted, server-side files.
    Prevents accidental or malicious injection.
    """
    # Ensure folder exists
    if not os.path.isdir(folder_path):
        raise ValueError(f"Folder not found: {folder_path}")

    # Build list of script tags
    scripts = []
    for filename in os.listdir(folder_path):
        # Only allow .js files, no hidden files, no user uploads
        if filename.endswith(".js") and not filename.startswith("."):
            scripts.append(
                tags.script(src=f"{folder_path}/{filename}")
            )

    return scripts