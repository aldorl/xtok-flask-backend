from dotenv import load_dotenv
import os
# Local packages
from config.paths import DIR_PATH, ASSETS_DIR, GENERATION_DIR, FRAMES_DIR
from twitter.api import authenticate_twitter, get_twitter_user, get_dummy_twitter_user
from twitter.models import get_user_display_pic, get_latest_tweet, get_timestamp_and_metrics
from image_processing.manipulations import get_final_image, save_final_image
from video_processing.loader import load_video
from video_processing.overlay import overlay_image_on_video, save_frames, write_frames_to_video

def main(dummy_data: bool = True):
    load_dotenv()

    # Authenticate with Twitter's API and get user details.
    if dummy_data:
        api = None
        user = get_dummy_twitter_user(user_handle='aldoruizluna')
    else:
        api = authenticate_twitter()
        user = get_twitter_user(api, user_handle='aldoruizluna')  # TODO: get this via frontend web app Twitter authentication

    # Fetch the latest tweet from the user's timeline and its details.
    latest_tweet = get_latest_tweet(api, user['screen_name'] if dummy_data else user.screen_name)
    tweet_text = latest_tweet['text'] if dummy_data else latest_tweet.text
    timestamp, metrics = get_timestamp_and_metrics(latest_tweet)

    # NOTE: For future implementation
    print("Metrics")
    print("=======")
    print(metrics)

    # Prepare the final image by drawing the user's info and tweet on the background image.
    background_image_path = os.path.join(DIR_PATH, ASSETS_DIR, 'background_image.png') # TODO: draw our own background_image, instead of using the static asset
    final_image = get_final_image(background_image_path, user, tweet_text, timestamp)

    # Fetch from Twitter and process a user's display picture.
    user_display_pic = get_user_display_pic(user)
    # Paste the user's display (profile) picture onto the final image at the specified position, using the profile picture as its own transparency mask.
    user_display_pic_position = (159, 610) #TODO: consider getting these coordinates dynamically
    final_image.paste(user_display_pic, user_display_pic_position, mask=user_display_pic)

    # Save the final image.
    generated_image = save_final_image(final_image)

    # Load a background video.
    background_video_path = os.path.join(DIR_PATH, ASSETS_DIR, 'background_video.mp4')
    background_video = load_video(background_video_path)

    # Overlay the generated image onto each frame of the background video.
    frames = overlay_image_on_video(background_video, generated_image)

    # Define path for saving individual frames and save sample frames as images.
    video_frames_path = os.path.join(DIR_PATH, FRAMES_DIR)
    save_frames(frames, video_frames_path)

    # Define path for final output video and convert frames to a video and save it.
    output_file_path = os.path.join(DIR_PATH, GENERATION_DIR, 'output_video.mp4')
    write_frames_to_video(frames, output_file_path)


# Runs the main function if the script is being run directly.
if __name__ == "__main__":
    main()
