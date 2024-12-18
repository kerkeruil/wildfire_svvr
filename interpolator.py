import cv2
import numpy as np
import os
from tqdm import tqdm
from PIL import Image

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

def interpolate_frames(frame1, frame2, alpha):
    # Calculate optical flow between two frames
    flow = cv2.calcOpticalFlowFarneback(
        cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY),
        cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY),
        None, 0.5, 3, 15, 3, 5, 1.2, 0
    )

    # Generate intermediate frame using alpha
    h, w = frame1.shape[:2]
    flow_map = np.zeros_like(frame1, dtype=np.float32)
    for y in range(h):
        for x in range(w):
            flow_map[y, x] = (1 - alpha) * frame1[y, x] + alpha * frame2[int(y + flow[y, x, 1]), int(x + flow[y, x, 0])]

    return flow_map.astype(np.uint8)


if __name__ == '__main__':
    os.makedirs("data/interpolated/", exist_ok=True)
    start_frame = cv2.imread("data/side_view_frames/1000.png")
    frames = os.listdir("data/side_view_frames")
    sorted_frames = sorted(frames, key=lambda x: int(x.split('.')[0])) # Sort by frame number

    for frame in tqdm(sorted_frames):
        end_frame = cv2.imread("data/side_view_frames/" + frame)
        intermediate_frame = interpolate_frames(start_frame, end_frame, 0.5)

        output_name = str(int(frame.split(".")[0]) + 500) + ".png"
        cv2.imwrite("data/interpolated/" + frame, start_frame)
        cv2.imwrite("data/interpolated/" + output_name, intermediate_frame)
        start_frame = end_frame
    create_animation("data/interpolated/", "data/full_interpolated.gif", duration=10)