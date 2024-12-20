import requests
from tqdm import tqdm
from pathlib import Path
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Download a file from a specified URL.")
parser.add_argument('--id', type=int, required=True, help='The ID of the file to download.')
parser.add_argument('--output_folder', type=str, default='data/', help='The folder to save the downloaded file.')

args = parser.parse_args()

id = args.id
file = f"output.{id}.vts"
output_folder = args.output_folder
url = f"https://visualisationlab.science.uva.nl/data/SciVisContest/2022/oceans11.lanl.gov/firetec/mountain_backcurve40/{file}"

os.makedirs(output_folder, exist_ok=True)

dest = Path(output_folder) / file

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
