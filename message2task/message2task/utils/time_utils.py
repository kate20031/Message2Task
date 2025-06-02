import re

def normalize_time(raw_time):
    if not raw_time:
        return None
    fixed_time = raw_time.replace('.', ':')
    match = re.match(r'^(\d{1,2}):(\d{1,2})$', fixed_time)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return f"{hours:02d}:{minutes:02d}"
    return None
