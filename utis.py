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

import re

def parse_timestamp(timestamp):
    patterns = [
        # r'(\d{1,2})h\s*(\d{1,2})m\s*(\d{1,2})s',  # hh mm ss
        r'(\d{1,2})\.(\d{1,2})\.(\d{1,2})',  # hh.mm.ss
        # r'(\d{1,2}):(\d{1,2}):(\d{1,2})',  # hh:mm:ss
        r'(\d{1,2})\.(\d{1,2})', # mm.ss
        # r'(\d{1,2})\:(\d{1,2})', # mm:ss
        r'(\d{1,2})' # ss

    ]

    for pattern in patterns:
        match = re.match(pattern, timestamp)
        hours = minutes = seconds = 0
        if match:
            groups = match.groups()
            if len(groups) == 3:
                hours, minutes, seconds = map(int, groups)
            elif len(groups) == 2:
                minutes, seconds = map(int, groups)
            elif len(groups) == 1:
                return int(groups[0])
            return (hours * 3600) + (minutes * 60) + seconds

    return None

def main():
    timestamp = input("Enter a timestamp (hh mm ss, hh.mm.ss, or hh:mm:ss): ")
    result = parse_timestamp(timestamp)
    if result is not None:
        print(f"Timestamp '{timestamp}' parsed to {result} seconds")
    else:
        print(f"Timestamp '{timestamp}' is invalid")

if __name__ == "__main__":
    main()

def find_file_with_prefix(prefix):
    # Get list of files in the directory
    files = os.listdir(Config.dir_path)

    # Filter files that start with the given prefix
    matching_files = [file for file in files if file.startswith(prefix)]
    return matching_files[0]

