from PIL import Image

def load_image(image_path: str) -> Image:
    """
    Open and return an image given its path.

    Parameters:
    image_path (str): Path to the image

    Returns:
    Image: An image object
    """
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        exit()