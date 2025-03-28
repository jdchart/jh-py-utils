import os
import zipfile

def collect_files(path, acceptedFormats = [], recursive = True):
    """Collect all files of accepted format in a given directory."""
    
    acceptedFormatsLower = {ext.lower() for ext in acceptedFormats}
    finalList = []
    
    if recursive:
        for root, _, files in os.walk(path):
            for file in files:
                if not acceptedFormats or os.path.splitext(file)[1][1:].lower() in acceptedFormatsLower:
                    finalList.append(os.path.join(root, file))
    else:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                if not acceptedFormats or os.path.splitext(file)[1][1:].lower() in acceptedFormatsLower:
                    finalList.append(full_path)
    
    return finalList

def zip_folder(path, zip_path):
    """Compress a folder as a zip file."""

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))