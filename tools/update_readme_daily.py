#!/usr/bin/env python3
"""
tools/update_readme_daily.py
Updates the dynamic "Daily Train Manifest" section of README.md based on current UTC date.
"""

from datetime import datetime, timezone
import os
import re
import sys

CHARACTERS = [
    ("Louis", "Main protagonist trying to escape the mysterious time loop aboard the Grekhov Express."),
    ("Dorothy", "Ticket Master / Conductor keeping order on the train amidst supernatural events."),
    ("Fedora", "Lead journalist for the Owlfeather, relentlessly seeking her big headline scoop."),
    ("Eduard", "Carriage 2 bartender who keeps track of everyone's drinking habits and secrets."),
    ("Jackie", "Attentive carriage staff tirelessly cleaning up shattered glass."),
    ("Shunyu", "Drunk high-stakes gambler whose mysterious murder sets the time loop in motion."),
    ("Kimmy", "Wealthy clock business heiress traveling in luxury Carriage 3."),
    ("Himmel", "Kimmy's anxious husband secretly harboring illicit contraband."),
    ("Sebastian", "Rigid and protective butler overseeing young Misha."),
    ("Misha", "A quiet child playing with wooden blocks; a surprisingly central figure."),
    ("Agatha", "Pragmatic assistant nurse tending to injured passengers in the staff cart."),
    ("Ichora", "Chief train engineer holding critical keys to restricted compartments."),
    ("Pattison", "Cryptic mail worker sorting letters while whispering mysterious rhymes."),
    ("Alexander", "Storage cart merchant dealing in banned super maple sugar.")
]

CARRIAGES = [
    ("Carriage 1 - Passenger Lounge", "The initial seating area where passengers gather and watch the mist pass by outside."),
    ("Carriage 2 - Dining & Casino Cart", "Home to Eduard's bar and Shunyu's high-stakes Mahjong games."),
    ("Carriage 3 - Luxury Cabins", "Opulent sleeper cabins reserved for high-profile figures like Kimmy and Himmel."),
    ("Carriage 4 - Staff & Infirmary", "Resting quarters for train personnel and Agatha's medical supply area."),
    ("Carriage 5 - Mail & Storage", "Pattison's domain filled with sorted parcels, contraband, and sealed crates."),
    ("Carriage 6 - The Sealed Locomotive", "The enigmatic front engine cart locked behind supernatural forces.")
]

CLUES = [
    "A shattered glass shard with faintly gleaming residue found near Carriage 2.",
    "A missing Mahjong tile bearing the '1-Bamboo' symbol tucked in a coat pocket.",
    "A faint smell of banned maple sugar lingering near the storage crates.",
    "An oversized pocket watch with hands stuck permanently at 4:00.",
    "A sealed letter with a broken wax symbol hidden beneath the conductor's desk.",
    "A cryptic rhyme scribbled on the reverse side of a train ticket.",
    "A heavy brass key with intricate engravings matching Carriage 6."
]

START_MARKER = "<!-- DAILY_UPDATE_START -->"
END_MARKER = "<!-- DAILY_UPDATE_END -->"

def generate_daily_content(today: datetime) -> str:
    day_of_year = today.timetuple().tm_yday

    char_name, char_desc = CHARACTERS[day_of_year % len(CHARACTERS)]
    carr_name, carr_desc = CARRIAGES[day_of_year % len(CARRIAGES)]
    clue = CLUES[day_of_year % len(CLUES)]
    date_str = today.strftime("%B %d, %Y")

    content = f"""{START_MARKER}
### 🚂 Daily Train Manifest & Mystery Report ({date_str})

> *"The Grekhov Express departs on schedule at 04:00. Watch the clock and check your ticket."*

* **📅 Today's Date:** `{date_str}` (UTC)
* **🔍 Featured Passenger:** **{char_name}** — *{char_desc}*
* **🚃 Carriage Spotlight:** **{carr_name}** — *{carr_desc}*
* **🧩 Daily Investigation Clue:** *"{clue}"*
* **⏰ Loop Status:** `ACTIVE` (Current Loop Iteration #{day_of_year})

---
{END_MARKER}"""
    return content

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    readme_path = os.path.join(repo_root, "README.md")

    if not os.path.exists(readme_path):
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_text = f.read()

    now = datetime.now(timezone.utc)
    new_daily_block = generate_daily_content(now)

    if START_MARKER in readme_text and END_MARKER in readme_text:
        pattern = re.compile(f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)
        updated_text = pattern.sub(new_daily_block, readme_text)
    else:
        target = "> *\"Departure at 4, embark on an epic adventure on board the Grekhov Express. Find the killer and untangle the mystery of the Grekhov and the dark secrets it contains...\"*\n\n---"
        replacement = f"{target}\n\n{new_daily_block}"
        if target in readme_text:
            updated_text = readme_text.replace(target, replacement, 1)
        else:
            updated_text = readme_text + "\n\n" + new_daily_block

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_text)

    print(f"Successfully updated README.md with daily manifest for {now.strftime('%Y-%m-%d')}.")

if __name__ == "__main__":
    main()
