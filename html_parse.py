import re
import csv
import os
import html
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
in_path = os.path.join(script_dir, 'history.html')
out_path = os.path.join(script_dir, 'history.csv')

with open(in_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

pattern = re.compile(
    r'Watched\s*<a href="(?P<link>https://www\.youtube\.com/watch\?v=[^"]+)">(?P<title>.*?)</a><br>'
    r'<a href="https://www\.youtube\.com/channel/[^"]+">(?P<creator>.*?)</a><br>'
    r'(?P<datetime>[^<]+)',
    re.DOTALL
)

matches = pattern.finditer(html_content)

with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'creator', 'link', 'datetime'])  # CSV header
    for match in matches:
        title = html.unescape(match.group('title'))
        creator = html.unescape(match.group('creator'))
        link = match.group('link')
        dt_raw = match.group('datetime').replace('\u202f', ' ').strip()
        dt_clean = dt_raw.rsplit(' ', 1)[0]  # Remove timezone abbreviation
        dt = match.group('datetime').replace('\u202f', ' ').strip()  # Normalize non-breaking space
        dt = datetime.strptime(dt_clean, "%b %d, %Y, %I:%M:%S %p")
        sortable_timestamp = dt.isoformat()  # For sorting
        writer.writerow([title, creator, link, sortable_timestamp])
