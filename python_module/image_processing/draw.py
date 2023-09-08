import tweepy
import textwrap
from typing import Any, Dict, Union
from PIL import Image, ImageDraw, ImageFont

def draw_text_on_image(draw: ImageDraw, position: tuple, text: str, font: ImageFont, color: tuple):
    """
    Draw a text on an image at a certain position, using a certain font and color.

    Parameters:
    draw (ImageDraw): ImageDraw instance to draw on
    position (tuple): Coordinates to place the text
    text (str): Text to be drawn
    font (ImageFont): Font to use
    color (tuple): Color for the text
    """
    draw.text(position, text, font=font, fill=color)

def draw_circular_mask(image: Image, size: tuple) -> Image:
    """
    Create a circular mask of a certain size for an image and apply it.

    Parameters:
    image (Image): Image to mask
    size (tuple): Desired size for the mask

    Returns:
    Image: Masked image
    """
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    image = image.resize(size)
    image.putalpha(mask)
    return image

def draw_wrapped_text_on_image(draw: ImageDraw, position: tuple, text: str, font: ImageFont, color: tuple, line_spacing: float):
    """
    Draw wrapped text on an image at a certain position, using a certain font, color, and line spacing.

    Parameters:
    draw (ImageDraw): ImageDraw instance to draw on
    position (tuple): Coordinates to place the text
    text (str): Text to be drawn
    font (ImageFont): Font to use
    color (tuple): Color for the text
    line_spacing (float): Space between lines
    """
    wrapped_text = wrap_text(text, 55)
    line_height = int(font.getbbox("hg")[3] * line_spacing)
    text_x, text_y = position
    for line in wrapped_text:
        draw.text((text_x, text_y), line, font=font, fill=color)
        text_y += line_height

def wrap_text(text: str, line_width: int, break_long_words: bool = False) -> list:
    """
    Split a text into lines of a certain width.

    Parameters:
    text (str): Text to be wrapped
    line_width (int): Maximum width of the lines
    break_long_words (bool): Whether to break words longer than line_width

    Returns:
    list: List of text lines
    """
    return textwrap.wrap(text, width=line_width, break_long_words=break_long_words)

def draw_user_info_and_tweet(draw: ImageDraw, user: Union[tweepy.models.User, Dict[str, Any]], tweet_text: str, timestamp: str):
    """
    Draw the user's info and tweet details onto the background image.

    Parameters:
    draw (ImageDraw): ImageDraw object
    user (Union[tweepy.models.User, Dict[str, Any]]): Twitter user object or a dictionary
    tweet_text (str): Text of the tweet
    timestamp (str): Formatted timestamp

    Returns:
    None
    """
    # Check if 'user' is a dictionary. If it is, then it's a dummy user
    if isinstance(user, dict):
        user_display_name = user['name']
        user_handle = "@" + user['screen_name']
    else:
        user_display_name = user.name
        user_handle = "@" + user.screen_name

    # Draw the user's display name on the background image.
    user_display_name_font = ImageFont.truetype("Arial", 26)
    user_display_name_position = (265, 619)
    user_display_name_color = (255, 255, 255)
    
    draw_text_on_image(draw, user_display_name_position, user_display_name, user_display_name_font, user_display_name_color)

    # Draw the user's handle on the background image.
    user_handle_font = ImageFont.truetype("Arial", 19)
    user_handle_position = (265, 660)
    user_handle_color = (109, 167, 204)

    draw_text_on_image(draw, user_handle_position, user_handle, user_handle_font, user_handle_color)

    # Draw a tweet text on the background image, splitting it into lines if necessary.
    tweet_text_font = ImageFont.truetype("Arial", 28)
    tweet_text_position = (159, 762)
    tweet_text_color = (255, 255, 255)
    
    draw_wrapped_text_on_image(draw, tweet_text_position, tweet_text, tweet_text_font, tweet_text_color, line_spacing=1.5)

    # Draw the timestamp on the background image.
    timestamp_font = ImageFont.truetype("Arial", 20)
    timestamp_position = (159, 1100.4)
    timestamp_color = (73, 75, 79)
    
    draw_text_on_image(draw, timestamp_position, timestamp, timestamp_font, timestamp_color)
