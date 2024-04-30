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
        user_state ={}
        for user in allowed_users:
            user_state[int(user)] = {'step':'link'}

def is_valid_youtube_link(url):
    # Regular expression to match YouTube URLs
    pattern = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
    # Check if the URL matches the pattern
    if re.match(pattern, url):
        return True
    else:
        return False

def parse_timestamp(timestamp):
    timestamp = timestamp.split(' ')
    time = 0
    for t in timestamp:
        if not t:
            continue
        if 'h' in t:
            time = time + (3600*int(t[:-1]))
        elif 'm' in t:
            time = time + (60*int(t[:-1]))
        elif 's' in t:
            time = time + int(t[:-1])
        else:
            return None
    return time

def find_file_with_prefix(prefix):
    # Get list of files in the directory
    files = os.listdir(Config.dir_path)

    # Filter files that start with the given prefix
    matching_files = [file for file in files if file.startswith(prefix)]
    return matching_files[0]

