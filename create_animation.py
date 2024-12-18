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
output_folder = "data\\animation\\"
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

        # Copy file to data/tmp 
        # This is in fact faster than loading it directly from the external drive by like 10 seconds
        shutil.copy(data_folder + f, tmp_folder)
        output_file = output_folder + f.split(".")[1] + ".png"
        renderer_obj.plot(tmp_folder + f, output_file=output_file)
        os.remove(os.path.join(tmp_folder, f))

        # Stats TODO: not tested
        frame_count += 1
        print("Time elapsed:", time.time() - start_time)
        print("avg time per frame:", round((time.time() - start_time) / frame_count,2), "seconds")
    
    create_animation(png_folder=output_folder, output_file='data\\topdown_view.gif', duration=400)







if __name__ == "__main__":
    main()
