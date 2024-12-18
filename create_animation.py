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
    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]
    png_files = sorted(png_files, key=lambda x: int(x.split('.')[0])) # Sort by frame number

    # Open images and append to list
    frames = []
    for file in png_files:
        img_path = os.path.join(png_folder, file)
        frame = Image.open(img_path)
        frames.append(frame)

    if frames:
        # Save as an animated GIF
        frames[0].save(output_file, save_all=True, append_images=frames[1:], duration=duration, loop=0)
        print(f"Animation saved as {output_file}")
    else:
        print("No PNG files found in the folder.")

def wind_origin_ranges(start, end, n_frames):
    ranges = []
    for b, e in zip(start, end):
        r = np.linspace(b, e, num=n_frames)
        ranges.append(r)

    return  np.array(ranges).T

def main():
    renderer_obj = renderer()
    os.makedirs(tmp_folder, exist_ok=True)
    all_timesteps = os.listdir(data_folder)[:10]
    existing_frames = os.listdir(side_output_folder)
    start_time = time.time()
    frame_count = 0
    wind_origins_1 = wind_origin_ranges([246, -10, 191], [27, 370, 220], len(all_timesteps))
    for i, f in enumerate(all_timesteps):
        print(f)
        if f.split(".")[1] + ".png" in existing_frames:
            print("Skipping:", f)   
            continue

        side_output_file = side_output_folder + f.split(".")[1] + ".png"
        topdown_output_file = topdown_output_folder + f.split(".")[1] + ".png"
        
        ## Direct from external drive
        renderer_obj.plot(data_folder + f, 
                          side_output_file=side_output_file, 
                          topdown_output_file=topdown_output_file, 
                          wind_origin=wind_origins[i]
                          )

        ## Copy file to local drive and then render
        ## This can be faster than loading it directly from the external drive
        # shutil.copy(data_folder + f, tmp_folder)
        # renderer_obj.plot(tmp_folder + f, output_file=output_file)
        # os.remove(os.path.join(tmp_folder, f))

        # Stats
        frame_count += 1

        avg_time = round((time.time() - start_time) / frame_count,1)
        print("Time elapsed:", round((time.time() - start_time)/60,1), "minutes")
        print("avg time per frame:", avg_time, "seconds\n")

        # Something is stored somewhere in memory, so we need to reset the renderer object
        # TODO: Find out what that is 
        if frame_count > 10:
            break

    shutil.rmtree(tmp_folder)
    create_animation(png_folder=side_output_folder, output_file='data\\test.gif', duration=10)


if __name__ == "__main__":
    main()
