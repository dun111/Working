#!/usr/bin/env python3
"""
tools/update_readme_daily.py

Automated script to update README.md daily with dynamic content,
including daily date badges, daily train logs, rotating character spotlights,
and mystery investigation tips.
"""

import os
import re
from datetime import datetime, timezone

# Rotation data for daily content updates
PASSENGER_SPOTLIGHTS = [
    {
        "name": "Louis",
        "role": "Protagonist & Investigator",
        "quote": "I woke up on this train with no memory, but I won't stop until I find the truth.",
        "tip": "Check Carriage 1 for initial clues before the time loop resets your progress."
    },
    {
        "name": "Dorothy",
        "role": "Train Conductor",
        "quote": "Tickets, please! The Grekhov Express operates on a strict schedule... loop or no loop.",
        "tip": "Dorothy knows the layout of every carriage. Ask her about train history."
    },
    {
        "name": "Shunyu",
        "role": "High-Stakes Gambler",
        "quote": "Luck is just a tile away... until the lights go out.",
        "tip": "Investigate the Mahjong tile found near the crime scene in Carriage 2."
    },
    {
        "name": "Fedora",
        "role": "Lead Journalist of The Owlfeather",
        "quote": "There is a story brewing on Carriage 3, and I intend to publish it.",
        "tip": "Fedora keeps detailed notes on all passengers. She may possess crucial alibis."
    },
    {
        "name": "Eduard",
        "role": "Carriage 2 Bartender",
        "quote": "Everyone talks to the bartender eventually. Drink or secret, what's your order?",
        "tip": "Eduard observes passenger movements in the dining cart throughout the evening."
    },
    {
        "name": "Kimmy",
        "role": "Clock Business Heiress",
        "quote": "Time is precious, especially when it keeps repeating itself.",
        "tip": "Examine the clockwork mechanics in the luxury cabin for hidden compartments."
    },
    {
        "name": "Misha",
        "role": "Passenger in Sleeper Cabin",
        "quote": "The blocks tell a story... if you know how to build them.",
        "tip": "Misha's building blocks contain subtle hints about the carriage layout."
    }
]

TRAIN_LOGS = [
    "The train passes through misty snow covered tracks as passenger whispers echo through Carriage 2.",
    "A mysterious chime echoes through the dining cart. Clockwork gears turn in silent sync.",
    "The lights in Carriage 5 flicker briefly. Time seems to stretch as the loop resets.",
    "Cold wind rattles the window panes of the staff cart. Clues lie waiting to be uncovered.",
    "Mahjong tiles clatter softly in the background. The victim's last trail remains intact.",
    "Carriage 6 remains locked from the inside. Only a sharp mind will earn the key.",
    "Midnight approaches aboard the Grekhov Express. The mystery deepens with every mile."
]

def generate_daily_readme():
    today = datetime.now(timezone.utc)
    date_str = today.strftime("%Y-%m-%d")
    formatted_date = today.strftime("%B %d, %Y")
    day_index = today.toordinal()

    spotlight = PASSENGER_SPOTLIGHTS[day_index % len(PASSENGER_SPOTLIGHTS)]
    log_entry = TRAIN_LOGS[day_index % len(TRAIN_LOGS)]

    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    readme_path = os.path.abspath(readme_path)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update or add Daily Update badge
    badge_str = f"![Daily Update](https://img.shields.io/badge/Daily%20Update-{date_str}-blue)"
    if "![Daily Update]" in content:
        content = re.sub(r"!\[Daily Update\]\(https://img\.shields\.io/badge/Daily%20Update-[^\)]+\)", badge_str, content)
    else:
        # Insert badge right after Status badge
        content = content.replace("![Status]", f"{badge_str}\n![Status]")

    # Daily Section content
    daily_section = f"""## 📅 Daily Grekhov Express Log ({formatted_date})

> **Current Train Log:** *"{log_entry}"*

### 🔍 Daily Passenger Spotlight: {spotlight['name']}
- **Role:** {spotlight['role']}
- **Passenger Quote:** *"{spotlight['quote']}"*
- **Investigation Tip:** {spotlight['tip']}

---
"""

    # Replace existing Daily section or insert above Release Announcement
    if "## 📅 Daily Grekhov Express Log" in content:
        content = re.sub(
            r"## 📅 Daily Grekhov Express Log \(.*?\)\n\n> \*\*Current Train Log:\*\*.*?\n\n---\n",
            daily_section,
            content,
            flags=re.DOTALL
        )
    else:
        content = content.replace("## 📢 Release Announcement", f"{daily_section}\n## 📢 Release Announcement")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully updated README.md for {date_str}.")

if __name__ == "__main__":
    generate_daily_readme()
