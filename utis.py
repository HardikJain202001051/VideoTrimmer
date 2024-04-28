import re
import json
class Config:
    """
    token: Unique ID of telegram Bot
    dir_path:  dir where downloaded videos will be stored
    """
    with open('config.json') as f:
        config = json.load(f)
        dir_path = config['videos_path']
        token = config['token']
        allowed_users = config['allowed_users']


def is_valid_youtube_link(url):
    # Regular expression to match YouTube URLs
    pattern = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
    # Check if the URL matches the pattern
    if re.match(pattern, url):
        return True
    else:
        return False

def check_timestamp(timestamp):
    timestamp = timestamp.split('.')
    if len(timestamp) > 3:
        return None
    for i in timestamp:
        if len(i) > 2 or not i.isdigit():
            return None
    return ':'.join(timestamp)

def get_timestamp(text):
    if len(text)<3:
        start = 0
    else:
        start = check_timestamp(text[1])
    end = check_timestamp(text[-1])
    return start,end

