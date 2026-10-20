#!/usr/bin/env python3
"""
update_readme_daily.py

Automated tool for updating the daily status, spotlight character,
carriage feature, daily quote, and dev log date in README.md.
"""

import datetime
import os
import re

CARRIAGE_ROTATION = [
    "Carriage 1 — First Class",
    "Carriage 2 — The Lounge",
    "Carriage 3 — Sleeper Cabins",
    "Carriage 4 — Staff Cart",
    "Carriage 5 — The Mail Room",
    "Carriage 6 — The Dark End",
]

CHARACTER_ROTATION = [
    ("Louis", "Main protagonist trying to solve the mystery of the time loop."),
    ("Dorothy", "Conductor on the Grekhov Express checking tickets."),
    ("Fedora", "Owlfeather journalist looking for the big story."),
    ("Eduard", "Bartender who knows everyone's drinks and secrets."),
    ("Shunyu", "High-stakes gambler looking for his next jackpot."),
    ("Kimmy", "Clock business heiress traveling in luxury."),
    ("Himmel", "Kimmy's anxious husband seeking solace."),
    ("Sebastian", "Protective butler overseeing Misha."),
    ("Misha", "Quiet child playing with blocks in Carriage 3."),
    ("Agatha", "Pragmatic nurse on duty in the staff cart."),
    ("Ichora", "Engineer holding the key to Carriage 6."),
    ("Pattison", "Mail worker murmuring cryptic rhymes."),
    ("Alexander", "Merchant trading in contraband maple sugar."),
]

QUOTES = [
    "\"The train doesn't forgive wrong guesses.\"",
    "\"Thank you for boarding the Grekhov Express.\"",
    "\"Not yet! Try to see the truth before you see the future.\"",
    "\"Every departure on it is printed the same way: 4:00.\"",
    "\"Don't hesitate.\"",
    "\"Truth accepted. Come see what you've won.\"",
]

def get_daily_content(dt: datetime.date):
    day_idx = dt.toordinal()
    carriage = CARRIAGE_ROTATION[day_idx % len(CARRIAGE_ROTATION)]
    char_name, char_desc = CHARACTER_ROTATION[day_idx % len(CHARACTER_ROTATION)]
    quote = QUOTES[day_idx % len(QUOTES)]

    date_formatted = dt.strftime("%A, %b %d, %Y")
    badge_date = dt.strftime("%A, %b %d, %Y")

    return {
        "date_str": date_formatted,
        "badge_date": badge_date,
        "carriage": carriage,
        "char_name": char_name,
        "char_desc": char_desc,
        "quote": quote,
    }

def update_readme(readme_path: str):
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    dt = datetime.date.today()
    info = get_daily_content(dt)

    # Replace badge
    content = re.sub(
        r"!\[Daily Update\]\(https://img\.shields\.io/badge/Daily%20Update-[^)]+\)",
        f"![Daily Update](https://img.shields.io/badge/Daily%20Update-{info['badge_date'].replace(' ', '%20').replace(',', '%2C')}-blueviolet)",
        content
    )

    # Replace section header
    content = re.sub(
        r"## 📅 Daily Update & Dev Log \([^)]+\)",
        f"## 📅 Daily Update & Dev Log ({info['date_str']})",
        content
    )

    # Replace daily status lines
    content = re.sub(
        r"> \*\* spotlight of the Day:\*\* .*",
        f"> ** spotlight of the Day:** **{info['carriage']}**  ",
        content
    )
    content = re.sub(
        r"> \*\* Featured Character of the Day:\*\* .*",
        f"> ** Featured Character of the Day:** **{info['char_name']}** — *\"{info['char_desc']}\"*  ",
        content
    )
    content = re.sub(
        r"> \*\* Daily Quote:\*\* .*",
        f"> ** Daily Quote:** *{info['quote']}*  ",
        content
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully updated {readme_path} for {info['date_str']}")
    return True

if __name__ == "__main__":
    readme_location = os.path.join(os.path.dirname(__file__), "..", "README.md")
    update_readme(readme_location)
