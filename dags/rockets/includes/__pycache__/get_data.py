# includes/get_data.py

import time
from urllib import request
from urllib.error import HTTPError

def check_file_exists(base_url, file_name):
    """
    Checks if the given file exists in the specified directory.
    """
    try:
        print(f"Checking if the file {file_name} exists in the directory {base_url}...")
        response = request.urlopen(base_url)
        directory_listing = response.read().decode('utf-8')

        if file_name not in directory_listing:
            raise FileNotFoundError(f"{file_name} is not available in {base_url}")
        
        print(f"File {file_name} is available.")
        return True
    except Exception as e:
        print(f"Error while checking file availability: {e}")
        raise

def download_file(url, output_path, max_retries=5):
    """
    Downloads a file from the given URL to the specified output path with retry logic.
    """
    retry_delay = 10  # Initial delay of 10 seconds

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}: Downloading data from {url}")
            request.urlretrieve(url, output_path)
            print(f"Data downloaded successfully and saved to {output_path}")
            return
        except HTTPError as e:
            if e.code == 503:
                print(f"Service unavailable (503). Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"Failed to download data from {url}: {e}")
                raise
        except Exception as e:
            print(f"Failed to download data from {url}: {e}")
            raise
    else:
        raise Exception(f"Failed to download data from {url} after {max_retries} attempts")
