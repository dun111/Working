#!/usr/bin/env python3
"""
tools/update_readme_daily.py
Automated script to update README.md every day with rotating daily content
(Featured Passenger, Mystery Quote/Clue, Daily Investigation Tip, Loop Status, etc.)
for 'Departure at 4' visual novel.
"""

import datetime
import hashlib
import os

PASSENGERS = [
    {
        "name": "Louis",
        "role": "Main Protagonist",
        "quote": "Huh, I don't remember how I got here... Man, this seems familiar.",
        "location": "Carriage 1 (Sleeper)",
        "tip": "Check interactive hotspots in every carriage to uncover clues about the loop."
    },
    {
        "name": "Dorothy",
        "role": "Ticket Master / Conductor",
        "quote": "Excuse me sir, tickets please. I'm not paid enough for this...",
        "location": "Carriage 1 (Entry)",
        "tip": "Dorothy knows the passenger manifest inside out. Re-interview staff after the murder."
    },
    {
        "name": "Fedora",
        "role": "Lead Journalist (The Owlfeather)",
        "quote": "I CAN'T WAIT to interview the KILLER.",
        "location": "Carriage 1 (Lounge)",
        "tip": "Journalists notice details others miss. Keep track of timeline shifts in dialogue."
    },
    {
        "name": "Eduard",
        "role": "Bartender",
        "quote": "I don't leave this counter during service, ask anyone.",
        "location": "Carriage 2 (Bar)",
        "tip": "Eduard monitors everyone's drinking habits. Verify alibis against bar tabs."
    },
    {
        "name": "Shunyu",
        "role": "High-Stakes Gambler",
        "quote": "Playing Mahjong! Doncha just love winning! Yes! I can't stop winning!",
        "location": "Carriage 2 (Dining Cart)",
        "tip": "Inspect Shunyu's Mahjong tile carefully; mismatched tiles hold the key to the mystery."
    },
    {
        "name": "Kimmy",
        "role": "Clock Business Heiress",
        "quote": "My family has a clock business, so we're quite well off.",
        "location": "Carriage 3 (Luxury Cabin)",
        "tip": "Clockwork precise timing is crucial when calculating time-loop loops."
    },
    {
        "name": "Himmel",
        "role": "Heiress's Husband",
        "quote": "W-what do you want, stranger? There's always a next stop...",
        "location": "Carriage 3 (Luxury Cabin)",
        "tip": "Look out for discarded drug wrappers and nervous behavior."
    },
    {
        "name": "Sebastian",
        "role": "Rigid Butler",
        "quote": "If any harm or distress befalls the child, you will be prosecuted.",
        "location": "Carriage 3 (Sleeper Cabin)",
        "tip": "A loyal butler rarely strays from his post unless drawn away by design."
    },
    {
        "name": "Misha",
        "role": "Mysterious Child",
        "quote": "They always come back. Don't they?",
        "location": "Carriage 3 (Playing Area)",
        "tip": "Check under Misha's carpet for hidden Mahjong tiles or items."
    },
    {
        "name": "Agatha",
        "role": "Assistant Nurse",
        "quote": "I deal with bodies, not motives. Put the bandaid on and stop wasting my time.",
        "location": "Carriage 4 (Staff Cart)",
        "tip": "Agatha's medical insight reveals if a victim was moved post-mortem."
    },
    {
        "name": "Ichora",
        "role": "Train Engineer",
        "quote": "The name's Ichora, I'm the train's engineer. Don't hesitate.",
        "location": "Carriage 4 (Engine Room)",
        "tip": "The engineer holds the critical key required to unlock Carriage 6."
    },
    {
        "name": "Pattison",
        "role": "Cryptic Mail Worker",
        "quote": "This goes to the clock, while this goes to the end.",
        "location": "Carriage 5 (Mail Room)",
        "tip": "Pattison notices creaking doors and footsteps along the mail carriage."
    },
    {
        "name": "Alexander",
        "role": "Storage Merchant",
        "quote": "The banned super maple sugar!!! First one is free, next one is 2000 perkels.",
        "location": "Carriage 5 (Storage Cart)",
        "tip": "Alexander knows who owes money on board and sells contraband goods."
    }
]

INVESTIGATION_NOTES = [
    "The time loop resets after reaching Carriage 5. Keep track of what changed between loops!",
    "Pay attention to Mahjong tile patterns; a mismatched tile in the victim's hand is vital evidence.",
    "Banned maple sugar wrappers point to illicit transactions aboard the Grekhov Express.",
    "Wrong accusations in the climax lead to immediate catastrophe—review all clues pressing 'J'.",
    "Carriage 6 remains locked until all clues are gathered and the real culprit is identified."
]

def get_daily_index(date_str, list_len):
    """Generate a deterministic index from the date string."""
    hash_val = int(hashlib.md5(date_str.encode('utf-8')).hexdigest(), 16)
    return hash_val % list_len

def generate_readme():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    formatted_date = now_utc.strftime("%B %d, %Y")

    passenger_idx = get_daily_index(date_str, len(PASSENGERS))
    featured = PASSENGERS[passenger_idx]

    note_idx = get_daily_index(date_str + "-note", len(INVESTIGATION_NOTES))
    featured_note = INVESTIGATION_NOTES[note_idx]

    readme_content = f"""# Departure at 4

![Status](https://img.shields.io/badge/Status-Release%20Coming%20Soon-yellow)
![Made with Ren'Py](https://img.shields.io/badge/Made%20with-Ren'Py-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Genre](https://img.shields.io/badge/Genre-Mystery%20%7C%20Visual%20Novel-purple)
![Resolution](https://img.shields.io/badge/Resolution-1920x1080-brightgreen)
![Daily Update](https://img.shields.io/badge/Loop%20Date-{date_str}-blueviolet)

> *"Departure at 4, embark on an epic adventure on board the Grekhov Express. Find the killer and untangle the mystery of the Grekhov and the dark secrets it contains..."*

---

## 🔄 Daily Loop Dispatch ({formatted_date})

> **📅 Last Updated:** {formatted_date} (UTC)
> **🕵️ Daily Passenger Spotlight:** **{featured['name']}** ({featured['role']})
> **📍 Primary Location:** {featured['location']}
> **💬 Featured Quote:** *"{featured['quote']}"*
> **💡 Investigation Tip:** {featured['tip']}
> **🔍 Daily Mystery Note:** {featured_note}

---

## 📢 Release Announcement

> **🚀 Release Coming Soon!**
> *Departure at 4* is currently in active development by **Blackberry Studios** (Version 1.5 Alpha). Stay tuned for upcoming build releases and distribution updates!

---

## 📖 Overview & Synopsis

**Departure at 4** is a story-rich, mystery visual novel developed in [Ren'Py](https://www.renpy.org/). Built for a native **1920 x 1080** display, the game combines interactive train carriage exploration, branching dialogue choices, clue gathering, and time-loop investigation mechanics.

### Storyline
You play as **Louis**, a young man who awakens violently aboard the moving **Grekhov Express** with no memory of how he arrived. As Louis explores the train's carriages—from the dining cart to the luxury sleeper cabins, staff carts, and mail rooms—he meets an unusual cast of characters.

However, after reaching the end of Carriage 5, a strange force sends Louis back to the beginning. Now trapped in a sinister **Time Loop** ("The Loop"), the train's lights dim, the atmosphere turns eerie, and a murder takes place: **Shunyu**, the high-stakes gambler, is found dead in Carriage 2 with a shard of glass in his side and a Mahjong tile placed in his palm.

Louis must re-interview passengers, uncover hidden clues (such as contraband banned maple sugar and hidden Mahjong tiles), and solve the murder mystery before confronting the supernatural truth awaiting in **Carriage 6**.

---

## 🎮 How to Play

### Gameplay Flow
1. **Explore Carriages:** Use interactive point-and-click hotspots on each carriage map to inspect objects, open doors, and examine crime scene details.
2. **Talk to Passengers:** Interrogate the passengers and train staff to learn about their background, motives, and alibis.
3. **Make Choices:** Select dialogue choices during interactions. Certain choices will branch dialogue or grant specific clues.
4. **Play Minigames:** Participate in interactive minigames such as the Mahjong tile-matching minigame in Carriage 2.
5. **Investigate the Loop:** After the time loop triggers, re-examine previously visited carriages for altered conditions, missing evidence, and hidden clues.
6. **Accuse the Killer:** At the climax, evaluate all collected clues and choose who committed the murder. An incorrect accusation results in immediate death, while the correct choice unlocks Carriage 6 for the final confrontation.

### Game Controls
| Input | Action |
| --- | --- |
| **Left Click / Space / Enter** | Advance dialogue / Select choices / Interact with hotspots |
| **Escape / Right Click** | Open Game Menu (Save, Load, Preferences, Quit) |
| **Ctrl (Hold)** | Fast Forward / Skip seen text |
| **Tab** | Toggle dialogue skipping |
| **Mouse Wheel** | Scroll back to view dialogue history |

---

## 👥 Character Directory

| Character | Role / Description |
| --- | --- |
| **Louis** | Main protagonist; wakes up aboard the train trying to get home, turned investigator |
| **Dorothy** | Ticket master / Train conductor on the Grekhov Express |
| **Fedora** | Lead journalist of the Owlfeather seeking her big headline scoop |
| **Eduard** | Carriage 2 bartender who knows everyone's drinking habits and tabs |
| **Jackie** | Carriage staff cleaning up shattered glass |
| **Shunyu** | Drunk, high-stakes Mahjong gambler; the murder victim in the Loop |
| **Kimmy** | Wealthy clock business heiress traveling in the luxury cabin |
| **Himmel** | Kimmy's anxious husband who secretly uses banned substances |
| **Sebastian** | Rigid and protective butler overseeing young Misha |
| **Misha** | Quiet child playing with blocks in the sleeper cabin; key murder suspect |
| **Agatha** | Pragmatic assistant nurse on board the staff cart |
| **Ichora** | Train engineer who gives Louis the critical key |
| **Pattison** | Cryptic mail worker who sorts letters and murmurs rhymes |
| **Alexander** | Storage cart merchant selling contraband "banned super maple sugar" |

---

## 💻 System Specifications

### Minimum System Requirements
| Component | Minimum Requirement | Recommended |
| --- | --- | --- |
| **OS** | 64-bit Windows 10, macOS 11 (Big Sur)+, or 64-bit Linux | Windows 11 / Current macOS |
| **Processor** | Dual-core CPU (~2.0 GHz or newer) | Quad-core CPU |
| **Memory (RAM)** | 4 GB RAM | 8 GB RAM |
| **Graphics** | Built-in graphics supporting OpenGL 2.0 or DirectX 11 | Dedicated GPU or Apple Silicon / Recent Integrated GPU |
| **Storage** | 300 MB free space | 300 MB free space |
| **Display** | 1280×720 minimum | **1920×1080** (Native Thumbnail & Game Resolution) |

---

## 🚀 Running the Game

### Downloading Pre-Built Releases
To play the standalone game:
1. Navigate to the [Releases](../../releases) section of this repository.
2. Download the latest build package corresponding to your operating system (**Windows**, **macOS**, or **Linux**).
3. Extract the downloaded zip/archive.
4. Launch the executable (`DepartureAt4.exe` on Windows, `DepartureAt4.app` on macOS, or `DepartureAt4.sh` on Linux).

---

### Launching via Ren'Py SDK (Source / Development)
1. Download and install the [Ren'Py SDK](https://www.renpy.org/latest.html) (version 8.0 or newer).
2. Clone or extract this repository into your Ren'Py projects directory.
3. Launch the Ren'Py SDK and select **"Add Existing Project"**.
4. Select **"Departure at 4"** (folder: `Working`) and click **"Launch Project"**.

---

## 🛠️ Credits & Development Team

**Studio:** Blackberry Studios
**Engine:** Ren'Py (Python)

- **Direction & Design:** Eric Zheng
- **Programming & Scripting:** Eric Zheng, Ryan
- **Lead Graphic Designers:** Hannah, Aydin
- **Story & Writing:** Hannah
- **Character Design:** Hannah, Aydin
- **Map Design:** Aydin
- **R&D & Technical Support:** Eric Zheng
- **Financial & Budget Director:** Eric Zheng

---

## 📜 License

- Powered by [Ren'Py Visual Novel Engine](https://www.renpy.org/).
- © Blackberry Studios. All rights reserved.
"""
    return readme_content.strip() + "\n"

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(root_dir, "README.md")

    content = generate_readme()
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully updated {readme_path}")

if __name__ == "__main__":
    main()
