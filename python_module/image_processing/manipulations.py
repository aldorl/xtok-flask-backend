import os
import tweepy
from typing import Any, Dict, Union
from PIL import Image, ImageDraw
# Local modules
from .draw import draw_user_info_and_tweet
from .loader import load_image
from config.paths import DIR_PATH, GENERATION_DIR

def get_final_image(background_image_path: str, user: Union[tweepy.models.User, Dict[str, Any]], tweet_text: str, timestamp: str) -> Image:
    """
    Generate the final image by overlaying user information, the tweet, and the timestamp on a background image.
    Save the final image in the filesystem and return the Image object.

    Parameters:
    background_image_path (str): Path to the background image
    user (Union[tweepy.models.User, Dict[str, Any]]): Twitter user object or a dictionary containing user details
    tweet_text (str): The text content of the user's latest tweet
    timestamp (str): The timestamp of the user's latest tweet

    Returns:
    Image: The final image with the user information, tweet, and timestamp overlaid on the background image
    """

    # Load the background image.
    background_image = Image.open(background_image_path)
    
    # Create a drawable object from the loaded image which can be used to draw onto the image.
    draw = ImageDraw.Draw(background_image)

    # Draw the user's info and tweet on the background image.
    # TODO : Implement metrics to display
    draw_user_info_and_tweet(draw, user, tweet_text, timestamp)

    return background_image

def save_final_image(draw: ImageDraw) -> Image:
    """
    Save the final generated image with all the user and tweet details onto the background, onto the filesystem.

    Parameters:
    draw (ImageDraw): ImageDraw object

    Returns:
    Image: Final image with all the details
    """

    # Define the output path for the final image.
    generated_image_path = os.path.join(DIR_PATH, GENERATION_DIR, 'final_image.png')

    # Save the final image.
    draw.save(generated_image_path)

    # Load this generated image and convert to RGBA format for transparency.
    generated_image = load_image(generated_image_path).convert("RGBA")
    return generated_image
