#!/usr/bin/env python3
"""
tools/update_readme_daily.py

Updates README.md with daily rotating game content (passenger spotlights,
clues, train logs, and date stamp) for Departure at 4.
"""

from datetime import datetime, timezone
import os
import sys

CHARACTERS = [
    {
        "name": "Louis",
        "role": "Protagonist & Investigator",
        "location": "Carriage 1 - Passenger Cabin",
        "quote": "Awakens with no memory on the moving Grekhov Express. Seeking a way home through the loop."
    },
    {
        "name": "Dorothy",
        "role": "Ticket Master & Train Conductor",
        "location": "Carriage 1 - Entrance",
        "quote": "Maintains strict schedule order on the Grekhov Express and holds key conductor access."
    },
    {
        "name": "Fedora",
        "role": "Lead Journalist (Owlfeather)",
        "location": "Carriage 1 - Seating Area",
        "quote": "Constantly hunting for a front-page scoop on the aristocratic Grekhov family."
    },
    {
        "name": "Eduard",
        "role": "Bartender",
        "location": "Carriage 2 - Dining & Bar",
        "quote": "Observes every passenger's drinking habits and knows who frequented the bar before the loop."
    },
    {
        "name": "Jackie",
        "role": "Train Staff",
        "location": "Carriage 2 - Bar Lounge",
        "quote": "Cleans up shattered glassware and notices subtle discrepancies in passenger behavior."
    },
    {
        "name": "Shunyu",
        "role": "High-Stakes Gambler",
        "location": "Carriage 2 - Mahjong Table",
        "quote": "A reckless gambler whose fate becomes central to the murder mystery in Carriage 2."
    },
    {
        "name": "Kimmy",
        "role": "Clock Business Heiress",
        "location": "Carriage 3 - Luxury Sleeper",
        "quote": "Traveled aboard the luxury cabin with exquisite timepieces and high society secrets."
    },
    {
        "name": "Himmel",
        "role": "Anxious Husband",
        "location": "Carriage 3 - Luxury Cabin",
        "quote": "Nervously hides a addiction to banned contraband while shielding his family."
    },
    {
        "name": "Sebastian",
        "role": "Rigid Butler",
        "location": "Carriage 3 - Family Suite",
        "quote": "Protective overseer of young Misha, keeping strict boundaries with outsiders."
    },
    {
        "name": "Misha",
        "role": "Quiet Child",
        "location": "Carriage 3 - Sleeper Cabin",
        "quote": "Plays quietly with wooden blocks in the cabin; holds unexpected observations."
    },
    {
        "name": "Agatha",
        "role": "Assistant Nurse",
        "location": "Carriage 4 - Staff Cart",
        "quote": "Pragmatic medical assistant equipped with emergency supplies on board."
    },
    {
        "name": "Ichora",
        "role": "Train Engineer",
        "location": "Carriage 4 - Engine Control",
        "quote": "Monitors the train mechanics and holds access to essential carriage keys."
    },
    {
        "name": "Pattison",
        "role": "Mail Worker",
        "location": "Carriage 5 - Mail Room",
        "quote": "Sorts letters meticulously while uttering enigmatic rhymes about time."
    },
    {
        "name": "Alexander",
        "role": "Storage Merchant",
        "location": "Carriage 5 - Storage Cart",
        "quote": "Deals in contraband goods including illegal super maple sugar."
    }
]

CLUES = [
    "Carriage 1: A locked door leads forward. Dorothy holds conductor access, but Carriage 6 remains shrouded.",
    "Carriage 2: Mahjong tiles lie scattered near the bar. Shunyu was last seen arguing over a high-stakes wager.",
    "Carriage 3: Banned super maple sugar was found hidden behind the luxury cabin wall paneling.",
    "Carriage 4: Medical supplies are stocked in Agatha's cart, but a scalp-sharp edge leaves unanswered questions.",
    "Carriage 5: Reaching the end of Carriage 5 triggers a temporal distortion, resetting the train loop.",
    "Carriage 6: Beyond the mystery threshold awaits the truth behind the Grekhov Express secrets.",
    "Clue #1: Glass shards near Shunyu match a broken glass from Carriage 2's bar counter.",
    "Clue #2: A dragon-inscribed Mahjong tile was placed directly in the murder victim's palm.",
    "Clue #3: Himmel's luxury pocket watch stopped precisely at 04:00 AM."
]

START_MARKER = "<!-- DAILY_README_START -->"
END_MARKER = "<!-- DAILY_README_END -->"

def generate_daily_block(now=None):
    if now is None:
        now = datetime.now(timezone.utc)

    date_str = now.strftime("%Y-%m-%d")
    ordinal = now.date().toordinal()

    char_idx = ordinal % len(CHARACTERS)
    clue_idx = ordinal % len(CLUES)
    loop_cycle = (ordinal % 365) + 1

    char = CHARACTERS[char_idx]
    clue = CLUES[clue_idx]

    block = f"""{START_MARKER}
## 🚂 Daily Train Logs & Investigation Spotlight

> **Date:** {date_str} | **Loop Cycle:** #{loop_cycle}

### 🔍 Featured Passenger: {char['name']}
- **Role:** {char['role']}
- **Location:** {char['location']}
- **Note:** {char['quote']}

### 🕵️ Daily Clue & Investigation Tip
> *"{clue}"*

---
{END_MARKER}"""
    return block

def update_readme(readme_path="README.md"):
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    daily_block = generate_daily_block()

    if START_MARKER in content and END_MARKER in content:
        start_pos = content.find(START_MARKER)
        end_pos = content.find(END_MARKER) + len(END_MARKER)
        updated_content = content[:start_pos] + daily_block + content[end_pos:]
    else:
        target = "## 📢 Release Announcement"
        if target in content:
            updated_content = content.replace(target, daily_block + "\n\n" + target)
        else:
            updated_content = content + "\n\n" + daily_block

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Successfully updated {readme_path} with daily content.")

if __name__ == "__main__":
    readme_file = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    update_readme(readme_file)
