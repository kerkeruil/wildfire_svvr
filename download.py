import requests
from tqdm import tqdm
from pathlib import Path
import os


file = "output.1000.vts" # Range from 1000 - 76000 with steps of 1000
output_folder = "data/"
url = "https://visualisationlab.science.uva.nl/data/SciVisContest/2022/oceans11.lanl.gov/firetec/valley_losAlamos/" + file
os.makedirs(output_folder, exist_ok=True)

dest = Path(output_folder + file)

try:
    # Send a GET request to get the file size first
    with requests.get(url, stream=True, verify=False) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8 KB

        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as progress_bar:
            with open(dest, 'wb') as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
    print(f"File downloaded successfully as {dest}")

except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")
