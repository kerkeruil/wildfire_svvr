"""
NOTE:
Run with "pvpython" instead of "python"
"""

import os
from render_class import renderer
from PIL import Image
import os
import time
import numpy as np
import shutil
import sys

backcurve = 40

data_folder = f"D:\\wildfire_data\\backcurve_{backcurve}\\"
output_folder = f"data\\report_visualizations\\custom\\"

os.makedirs(output_folder, exist_ok=True)

def main():
    f = 35000
    filename = "frame_35_double_shifted_wind"
    p1 = np.array([[-493, -162, 204], [701, -162, 100]])
    p2 = np.array([[-493, 145, 204], [701, 145, 100]])

    # avg_p = (p1 + p2) / 2

    renderer_obj = renderer()
    renderer_obj.plot(
        data_folder + f"output.{f}.vts",
        side_output_file=output_folder + filename + "_side.png",
        topdown_output_file=output_folder + filename + "_topdown.png",
        wind_origins_p1_start=p1[0],
        wind_origins_p1_end=p1[1],
        wind_origins_p2_start=p2[0],
        wind_origins_p2_end=p2[1],
    )



if __name__ == "__main__":
    # Take in filename as argument
    main()
