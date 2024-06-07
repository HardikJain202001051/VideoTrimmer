import re
import json
import os

class Config:
    """
    token: Unique ID of telegram Bot
    dir_path:  dir where downloaded videos will be stored
    """
    with open('config.json') as f:
        config = json.load(f)
        dir_path = config['videos_path']
        token = config['token']
        allowed_users = set(map(int,config['allowed_users']))


def is_valid_youtube_link(url):
    # Regular expression to match YouTube URLs
    pattern = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
    # Check if the URL matches the pattern
    if re.match(pattern, url):
        return True
    else:
        return False

def parse_timestamp(timestamp):
    timestamp = timestamp.split('.')
    if len(timestamp) != 3:
        return None
    hours, minutes, seconds = timestamp
    if not (hours.isdigit() and minutes.isdigit() and seconds.isdigit()):
        return None
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)
    time = (hours * 3600) + (minutes * 60) + seconds
    return time

def find_file_with_prefix(prefix):
    # Get list of files in the directory
    files = os.listdir(Config.dir_path)

    # Filter files that start with the given prefix
    matching_files = [file for file in files if file.startswith(prefix)]
    return matching_files[0]

