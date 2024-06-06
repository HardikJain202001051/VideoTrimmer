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
    timestamp = timestamp.split(' ')
    time = 0
    for t in timestamp:
        p,s = t[:-1],t[-1]
        if not p.isidigit():
            return None
        p = int(p)
        if 'h' == s:
            time = time + (3600*p)
        elif 'm' == s:
            time = time + (60*p)
        elif 's' == s:
            time = time + p
        else:
            return None
    return time

def find_file_with_prefix(prefix):
    # Get list of files in the directory
    files = os.listdir(Config.dir_path)

    # Filter files that start with the given prefix
    matching_files = [file for file in files if file.startswith(prefix)]
    return matching_files[0]

