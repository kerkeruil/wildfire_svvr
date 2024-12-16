"""
NOTE:
Run with "pvpython" instead of "python"
"""


import os
from renderer import render
from pathlib import Path

data_folder = "data/raw/"
output_folder = "data/animation/"

os.makedirs(output_folder, exist_ok=True)

def main():
    for f in os.listdir(data_folder):
        print(f)
        if "6000.vts" not in f:
            continue
        output_file = output_folder + f.split(".")[1] + ".png"
        print(f"Rendering {f}...")
        render(filename=f, output_file=output_file)


if __name__ == "__main__":
    main()