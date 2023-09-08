import os
import json
import tweepy
from typing import Dict
# Local modules
from config.paths import DIR_PATH, DATA_DIR

def authenticate_twitter() -> tweepy.API:
    """
    Authenticate with Twitter's API and return the API object.

    Returns:
    tweepy.API: Authenticated Twitter API object
    """
    # Get Twitter API keys and tokens from environment variables
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Missing one or more Twitter API keys or tokens.")
        exit()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api

def get_twitter_user(api: tweepy.API, user_handle: str) -> tweepy.models.User:
    """
    Get the Twitter user details given a user handle.

    Parameters:
    api (tweepy.API): Authenticated Twitter API object
    user_handle (str): Twitter user handle

    Returns:
    tweepy.models.User: Twitter user object
    """
    try:
        user = api.get_user(screen_name=user_handle)
    except tweepy.TweepyException as e:
        print(f"Failed to get user {user_handle}. Error: {e}")
        exit()

    return user

def get_dummy_twitter_user(user_handle: str) -> Dict:
    """
    Get the dummy Twitter user details given a user handle.

    Parameters:
    user_handle (str): Twitter user handle

    Returns:
    Dict: Twitter user object as a dictionary
    """
    try:
        # Load dummy data from JSON file
        dummy_user_path = os.path.join(DIR_PATH, DATA_DIR, 'dummy_user.json')
        with open(dummy_user_path, 'r') as file:
            user = json.load(file)
    except FileNotFoundError as e:
        print(f"Failed to get user {user_handle}. Error: {e}")
        exit()

    return user
