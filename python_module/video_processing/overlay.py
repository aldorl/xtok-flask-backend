import cv2
import numpy as np
from PIL import Image

def overlay_image_on_video(video: cv2.VideoCapture, image: Image) -> list:
    """
    Overlay an image onto each frame of a video and return the resulting frames.

    Parameters:
    video (cv2.VideoCapture): Video onto which to overlay the image
    image (Image): Image to overlay

    Returns:
    list: List of frames with the image overlaid
    """
    frames = []
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_with_image = Image.fromarray(frame).convert("RGBA")
        result = Image.alpha_composite(frame_with_image, image)
        frames.append(np.array(result))
    video.release()
    return frames

def save_frames(frames: list, dir_path: str, num_frames_to_save: int = 2):
    """
    Save a certain number of frames as images in a certain directory for verification/preview purposes.

    Parameters:
    frames (list): List of frames to save
    dir_path (str): Directory to save the frames
    num_frames_to_save (int): Number of frames to save
    """
    for i, frame in enumerate(frames):
        if i < num_frames_to_save:
            image = Image.fromarray(frame)
            image.save(f"{dir_path}/frame_{i}.png")
        else:
            break

def write_frames_to_video(frames: list, output_path: str, fps: int = 30):
    """
    Convert a list of frames into a video and save it at a certain path.

    Parameters:
    frames (list): List of frames to convert to video
    output_path (str): Path to save the video
    fps (int): Frames per second for the video
    """
    if not frames:
        print("No frames to write.")
        return

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_size = (frames[0].shape[1], frames[0].shape[0])
    video = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    for frame in frames:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB) # Convert frame to RGB format
        video.write(frame_rgb)
    video.release()