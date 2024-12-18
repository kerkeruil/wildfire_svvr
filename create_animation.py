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


# data_folder = "data/raw/"
side_output_folder = "data\\side_frames\\"
topdown_output_folder = "data\\topdown_frames\\"
data_folder = "D:\\wildfire_data\\backcurve_40\\"
tmp_folder = "data\\tmp\\"

# data_folder = "data\\raw\\"

os.makedirs(side_output_folder, exist_ok=True)
os.makedirs(topdown_output_folder, exist_ok=True)


def create_animation(png_folder, output_file, duration=200):
    """
    Combine PNG files into an animated GIF.

    Args:
        png_folder (str): Path to the folder containing PNG files.
        output_file (str): Output file name (e.g., 'animation.gif').
        duration (int): Duration of each frame in milliseconds.
    """
    # Get list of PNG files and sort them
    png_files = [f for f in os.listdir(png_folder) if f.endswith(".png")]
    png_files = sorted(
        png_files, key=lambda x: int(x.split(".")[0])
    )  # Sort by frame number

    # Open images and append to list
    frames = []
    for file in png_files:
        img_path = os.path.join(png_folder, file)
        frame = Image.open(img_path)
        frames.append(frame)

    if frames:
        # Save as an animated GIF
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
        )
        print(f"Animation saved as {output_file}")
    else:
        print("No PNG files found in the folder.")


def wind_origin_ranges(start, end, n_frames):
    ranges = []
    for b, e in zip(start, end):
        r = np.linspace(b, e, num=n_frames)
        ranges.append(r)

    return np.array(ranges).T


def main():
    os.makedirs(tmp_folder, exist_ok=True)
    all_timesteps = os.listdir(data_folder)
    existing_frames = os.listdir(side_output_folder)
    start_time = time.time()
    frame_count = 0

    # Setup the shift of the wind origins
    wind_origins_p1_start = wind_origin_ranges(
        [-493, -60, 204], [-493, -384, 204], len(all_timesteps)
    )
    wind_origins_p1_end = wind_origin_ranges(
        [701, -60, 100], [701, -354, 100], len(all_timesteps)
    )

    wind_origins_p2_start = wind_origin_ranges(
        [-493, 60, 204], [-493, 350, 204], len(all_timesteps)
    )
    wind_origins_p2_end = wind_origin_ranges(
        [701, 60, 100], [701, 350, 100], len(all_timesteps)
    )

    # stream 1
    # [-493, -60, 204] [701, -60, 100]
    # [-493, -384, 204] [701, -354, 100]

    # stream 2
    # [-493, 60, 204] [701, 60, 100]
    # [-493, 350, 204] [701, 350, 100]

    # Render each frame
    renderer_obj = renderer()

    for i, f in enumerate(all_timesteps):
        if f.split(".")[1] + ".png" in existing_frames:
            print("Skipping:", f)
            continue

        side_output_file = side_output_folder + f.split(".")[1] + ".png"
        topdown_output_file = topdown_output_folder + f.split(".")[1] + ".png"

        ## Direct from external drive
        renderer_obj.plot(
            data_folder + f,
            side_output_file=side_output_file,
            topdown_output_file=topdown_output_file,
            wind_origins_p1_start=wind_origins_p1_start[i],
            wind_origins_p1_end=wind_origins_p1_end[i],
            wind_origins_p2_start=wind_origins_p2_start[i],
            wind_origins_p2_end=wind_origins_p2_end[i],
        )

        ## Copy file to local drive and then render
        ## This can be faster than loading it directly from the external drive
        # shutil.copy(data_folder + f, tmp_folder)
        # renderer_obj.plot(tmp_folder + f, output_file=output_file)
        # os.remove(os.path.join(tmp_folder, f))

        # Stats
        frame_count += 1

        avg_time = round((time.time() - start_time) / frame_count, 1)
        print("Time elapsed:", round((time.time() - start_time) / 60, 1), "minutes")
        print("avg time per frame:", avg_time, "seconds\n")

        # Something is stored somewhere in memory, so we need to reset the renderer object
        # TODO: Find out what that is

    shutil.rmtree(tmp_folder)
    # create_animation(png_folder=side_output_folder, output_file='data\\test.gif', duration=10)
    create_animation(
        png_folder=topdown_output_folder,
        output_file="data\\gifs\\topdown_final.gif",
        duration=10,
    )


if __name__ == "__main__":
    main()
