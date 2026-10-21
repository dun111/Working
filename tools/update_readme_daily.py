#!/usr/bin/env python3
"""
update_readme_daily.py

Updates README.md with the current date badge / 'Last Updated' timestamp.
"""

import os
import re
from datetime import datetime, timezone

def update_readme():
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")

    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    today_str = datetime.now(timezone.utc).strftime("%Y--%m--%d")
    date_badge = f"![Last Updated](https://img.shields.io/badge/Last%20Updated-{today_str}-blue)"

    # Regex to replace existing Last Updated badge or add it if not present
    badge_pattern = r"!\[Last Updated\]\(https://img\.shields\.io/badge/Last%20Updated-[^\)]+\)"

    if re.search(badge_pattern, content):
        new_content = re.sub(badge_pattern, date_badge, content)
    else:
        # Insert after the status badge or at the top after title
        status_pattern = r"(!\[Status\]\([^\)]+\)\n)"
        if re.search(status_pattern, content):
            new_content = re.sub(status_pattern, r"\1" + date_badge + "\n", content)
        else:
            new_content = date_badge + "\n\n" + content

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated README.md with date: {today_str}")

if __name__ == "__main__":
    update_readme()
