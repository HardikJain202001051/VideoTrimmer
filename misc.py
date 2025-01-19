import re

def int_or_zero(group):
    if group:
        return int(group)
    return 0
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

if __name__ == "__main__":

    print(parse_timestamp("2.0"))