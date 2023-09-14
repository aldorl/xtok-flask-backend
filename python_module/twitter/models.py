import os
import json
import tweepy
import requests
from io import BytesIO
from PIL import Image
from typing import Any, Dict, Union, Optional, Tuple
# Local modules
from config.paths import DIR_PATH, DATA_DIR
from image_processing.draw import draw_circular_mask

def get_user_display_pic(user: Union[tweepy.models.User, Dict[str, Any]]) -> Image:
    """
    Fetch and process a user's display picture.

    Parameters:
    user (Union[tweepy.models.User, Dict[str, Any]]): Twitter user object or a dictionary

    Returns:
    Image: Processed user's display picture
    """
    try:
        # Check if 'user' is a dictionary. If it is, then it's a dummy user
        if isinstance(user, dict):
            profile_image_url_https = user['profile_image_url_https']
        else:
            profile_image_url_https = user.profile_image_url_https

        response = requests.get(profile_image_url_https)
        user_display_pic = Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        print(f"Failed to get user's display picture. Error: {e}")
        exit()

    user_display_pic_size = (92, 92)
    user_display_pic = draw_circular_mask(user_display_pic, user_display_pic_size)

    return user_display_pic

def get_latest_tweet(api: Optional[tweepy.API], user_handle: str) -> Union[tweepy.models.Status, Dict[str, Any]]:
    """
    Fetch the latest tweet from the user's timeline.
    
    Parameters:
    api (Optional[tweepy.API]): Authenticated Twitter API object or None for dummy data
    user_handle (str): Twitter user handle

    Returns:
    Union[tweepy.models.Status, Dict[str, Any]]: Latest tweet object
    """
    try:
        if api is None:
            # Load dummy data from JSON file
            dummy_tweet_path = os.path.join(DIR_PATH, DATA_DIR, 'dummy_tweet.json')
            with open(dummy_tweet_path, 'r') as file:
                latest_tweet = json.load(file)
        else:
            latest_tweet = api.user_timeline(screen_name=user_handle, count=1)[0]
    except tweepy.TweepyException as e:
        print(f"Failed to get the latest tweet from {user_handle}. Error: {e}")
        exit()

    return latest_tweet

def get_timestamp_and_metrics(tweet: Union[tweepy.models.Status, Dict[str, Any]]) -> Tuple[str, str]:
    """
    Fetch the timestamp and other tweet metrics.

    Parameters:
    tweet (Union[tweepy.models.Status, Dict[str, Any]]): Twitter tweet object or a dictionary

    Returns:
    tuple[str, str]: Formatted timestamp and metrics
    """
    # TODO: format timestamp and metrics aesthetically
    # NOTE: sample timestamp + impressions (views) format
    ### "19:05 . 2023-06-23 . 21.9K Views" 
    if isinstance(tweet, dict):
        # If it's dummy data
        timestamp = tweet['created_at']
        metrics = tweet['metrics']
    else:
        # If it's a real tweet
        timestamp = str(tweet.created_at)
        # TODO: add quote tweets and impressions to metrics
        metrics = f"Replies: {tweet.reply_count}, Retweets: {tweet.retweet_count}, Likes: {tweet.favorite_count}"
    
    # TODO: get 'source' of tweet
    return timestamp, metrics
