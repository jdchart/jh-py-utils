import os
import requests
import zipfile
from requests.exceptions import ChunkedEncodingError, ConnectionError
import time

def download(url, **kwargs):
    if kwargs.get("dir", None) == None:
        dl_location = os.path.join(os.getcwd(), os.path.basename(url))
    else:
        dl_location = os.path.join(kwargs.get("dir"), os.path.basename(url))
    _download_online_file(url, dl_location, kwargs.get("range", None))
    return dl_location
    
# def _download_online_file(url, path, range):
#     """Download a file to base colab directory."""
#     if range == None:
#         response = requests.get(url, stream=True)
#     else:
#         response = requests.get(url, headers={'Range': f'bytes={range}'}, stream=True)
#     if response.status_code == 206 or response.status_code == 200:
#         with open(path, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=1024):
#                 file.write(chunk)
def _download_online_file(url, path, range=None, retries=3, backoff=2):
    """Download a file to base colab directory with retries on failures."""
    headers = {'Range': f'bytes={range}'} if range else {}
    
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            if response.status_code in (200, 206):
                with open(path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive chunks
                            file.write(chunk)
                return  # Success!
            else:
                print(f"Unexpected status code: {response.status_code}")
                break  # Don't retry on bad status codes
        except (ChunkedEncodingError, ConnectionError, requests.exceptions.ReadTimeout) as e:
            attempt += 1
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < retries:
                time.sleep(backoff * attempt)
            else:
                raise  # Let the final failure raise an error

def download_zip(url, path):
    """Download a zip file and unpack it's contents at the given path (a folder of the filename will be created)."""
    
    # Download file:
    response = requests.get(url)
    temp_zip = os.path.join(path, os.path.basename(url))
    with open(temp_zip, 'wb') as file:
        file.write(response.content)

    # Create the output folder:
    if os.path.isdir(path) == False:
        os.makedirs(path)

    # Unzip:
    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall(path)
    
    # Remove temporary ip file:
    os.remove(temp_zip)