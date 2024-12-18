"""
NOTE:
Run with "pvpython" instead of "python"
"""

import os
from render_class import renderer
from PIL import Image
import os
import time
import shutil


# data_folder = "data/raw/"
output_folder = "data\\side_view_frames\\"
data_folder = "D:\\wildfire_data\\"
tmp_folder = "data\\tmp\\"

# data_folder = "data\\raw\\"

os.makedirs(output_folder, exist_ok=True)

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

def main():
    renderer_obj = renderer()
    os.makedirs(tmp_folder, exist_ok=True)
    existing_frames = os.listdir(output_folder)
    start_time = time.time()
    frame_count = 0
    for f in os.listdir(data_folder):
        if "vts" not in f or f.split(".")[1] + ".png" in existing_frames:
            print("Skipping:", f)   
            continue

        output_file = output_folder + f.split(".")[1] + ".png"
        
        ## Direct from external drive
        renderer_obj.plot(data_folder + f, output_file=output_file)

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

    
    create_animation(png_folder=output_folder, output_file='data\\side_view.gif', duration=400)







if __name__ == "__main__":
    main()
