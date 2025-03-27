import os
import zipfile

def collect_files(path, acceptedFormats = []):
    """Collect all files of accepted format in a given directory."""

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if len(acceptedFormats) > 0:
                extension = os.path.splitext(file)[1][1:]
                if extension in acceptedFormats:
                    finalList.append(os.path.join(root, file))
            else:
                finalList.append(os.path.join(root, file))
    return finalList

def zip_folder(path, zip_path):
    """Compress a folder as a zip file."""

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))