"""
NOTE:
Run with "pvpython" instead of "python"
"""

import os
from render_class import renderer
from pathlib import Path

data_folder = "data/raw/"
output_folder = "data/animation/"

os.makedirs(output_folder, exist_ok=True)


def main():
    renderer_obj = renderer()
    for f in os.listdir(data_folder):
        print(f)
        if "vts" not in f:
            continue
        output_file = output_folder + f.split(".")[1] + ".png"
        renderer_obj.plot(f, output_file=output_file)


if __name__ == "__main__":
    main()
