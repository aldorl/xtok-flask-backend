import cv2

def load_video(video_path: str) -> cv2.VideoCapture:
    """
    Open and return a video given its path.

    Parameters:
    video_path (str): Path to the video

    Returns:
    cv2.VideoCapture: A video object
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Failed to open the video.")
        exit()
    return video