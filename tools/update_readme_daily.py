#!/usr/bin/env python3
"""
tools/update_readme_daily.py

Updates README.md with daily rotating content, such as Daily Spotlight,
Featured Character, Daily Investigation Clue, and Last Updated timestamp.
Designed to be run daily via GitHub Actions or locally.
"""

import datetime
import os
import re

START_TAG = "<!-- DAILY-UPDATE-START -->"
END_TAG = "<!-- DAILY-UPDATE-END -->"

SPOTLIGHTS = [
    {
        "character": "Dorothy",
        "role": "Train Conductor",
        "quote": "Tickets, please! The Grekhov Express operates on strict schedules, though time itself seems... slippery today.",
        "clue": "Carriage 1 ticket log shows an extra unregistered passenger checked in at 3:45 AM.",
        "status": "On Schedule - Carriage 1 Cleared"
    },
    {
        "character": "Fedora",
        "role": "Lead Journalist of the Owlfeather",
        "quote": "A murder on a moving train during a time loop? Now THAT is front-page headline material!",
        "clue": "An unprinted news draft found in the waste bin mentions a high-stakes Mahjong debt.",
        "status": "Investigation Active - Press Briefing Pending"
    },
    {
        "character": "Eduard",
        "role": "Carriage 2 Bartender",
        "quote": "Another drink? On this train, everybody has a tab, and everybody has a secret.",
        "clue": "Traces of illegal maple sugar substitute were found on a cocktail glass in Carriage 2.",
        "status": "Bar Open - High Tension in Dining Cart"
    },
    {
        "character": "Jackie",
        "role": "Carriage Staff",
        "quote": "Shattered glass again... no matter how many times I sweep, it's back after every reset.",
        "clue": "A glass shard missing from the dining cart lamp matches the weapon found at the crime scene.",
        "status": "Maintenance Duty - Glass Cleanup in Progress"
    },
    {
        "character": "Shunyu",
        "role": "High-Stakes Gambler",
        "quote": "Lady Luck is a fickle mistress, but tonight, the tiles speak to me.",
        "clue": "A unique bamboo-pattern Mahjong tile was discovered clenched in Shunyu's hand.",
        "status": "Crime Scene Under Lockdown - Carriage 2"
    },
    {
        "character": "Kimmy",
        "role": "Clock Business Heiress",
        "quote": "Time is precious, darling. And aboard this express, time is running out.",
        "clue": "A pocket watch stopped precisely at 4:00 AM was recovered from the luxury cabin.",
        "status": "Resting in Luxury Suite - Guarded"
    },
    {
        "character": "Alexander",
        "role": "Storage Merchant",
        "quote": "Banned super maple sugar? I don't know what you're talking about... unless you have the cash.",
        "clue": "A crate marked 'Confectionery' in Storage Cart contains suspicious smuggled contraband.",
        "status": "Storage Vault Open for Trade"
    }
]

def generate_daily_content(today: datetime.date) -> str:
    # Use day of year to deterministically pick today's spotlight
    day_index = today.timetuple().tm_yday % len(SPOTLIGHTS)
    spot = SPOTLIGHTS[day_index]
    date_str = today.strftime("%Y-%m-%d")

    content = f"""{START_TAG}
### 🕵️ Daily Express Dispatch ({date_str})

> **📅 Today's Featured Passenger:** **{spot['character']}** (*{spot['role']}*)
> **💬 Quote of the Day:** *"{spot['quote']}"*
> **🔍 Daily Investigation Clue:** `{spot['clue']}`
> **📊 Grekhov Express Status:** `{spot['status']}`

*This section updates daily automatically at 00:00 UTC via GitHub Actions.*
{END_TAG}"""
    return content

def update_readme(filepath="README.md"):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        readme_text = f.read()

    today = datetime.datetime.now(datetime.timezone.utc).date()
    new_daily_block = generate_daily_content(today)

    if START_TAG in readme_text and END_TAG in readme_text:
        pattern = re.compile(f"{re.escape(START_TAG)}.*?{re.escape(END_TAG)}", re.DOTALL)
        updated_text = pattern.sub(new_daily_block, readme_text)
    else:
        # Insert after overview section or at top under header
        heading_match = re.search(r"(## 📢 Release Announcement)", readme_text)
        if heading_match:
            pos = heading_match.start()
            updated_text = readme_text[:pos] + new_daily_block + "\n\n---\n\n" + readme_text[pos:]
        else:
            updated_text = readme_text + "\n\n" + new_daily_block

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_text)

    print(f"Successfully updated {filepath} for {today.strftime('%Y-%m-%d')}.")
    return True

if __name__ == "__main__":
    update_readme()
