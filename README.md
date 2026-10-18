# Departure at 4: Every Day Changing It

![Status](https://img.shields.io/badge/Status-Version%202.0%20Beta-yellow)
![Made with Ren'Py](https://img.shields.io/badge/Made%20with-Ren'Py%208.0+-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Genre](https://img.shields.io/badge/Genre-Mystery%20%7C%20Time%20Loop%20%7C%20Horror-purple)
![Resolution](https://img.shields.io/badge/Resolution-1920x1080-brightgreen)

> *"Departure at 4: embark on an epic mystery aboard the Grekhov Express. Trapped in a loop where every day changes reality, find the killer and untangle dark supernatural secrets..."*

---

## 📢 Release Announcement

> **🚀 Departure at 4 — Version 2.0 Beta**
> Developed by **Blackberry Studios**. Explore the mysterious Grekhov Express, navigate shifting time loops, solve murder investigations, play casino minigames, and unlock hidden secrets!

---

## 📖 Overview & Synopsis

**Departure at 4: Every Day Changing It** (internal project title: *Working*) is a story-rich mystery visual novel with psychological horror and time-loop investigation mechanics built in [Ren'Py](https://www.renpy.org/). Designed natively for **1920 × 1080** displays, the game mixes interactive train carriage exploration, branching interrogations, clue discovery, minigames, and secret achievements.

### Storyline
You play as **Louis**, a young man who wakes up aboard the speeding **Grekhov Express** with no memory of how he boarded. As Louis explores the train's carriages—from the dining cart to luxury sleeper cabins, staff carts, and mail rooms—he encounters an intriguing cast of passengers and crew members.

However, upon reaching Carriage 5, an enigmatic force resets time, thrusting Louis into **"The Loop"**. With every cycle, conditions aboard the train shift:
- **Every Day Changing:** Lights dim, eerie shadows loom, dialogue options alter, and crime scenes transform.
- **The Murder Mystery:** **Shunyu**, the high-stakes gambler, is found murdered in Carriage 2 with a shard of glass in his side and a Mahjong tile placed in his hand.
- **Investigation:** Louis must re-interrogate passengers, uncover hidden clues (such as banned maple sugar contraband and hidden Mahjong tiles), navigate horror visions, and identify the killer to unlock **Carriage 6** for the ultimate supernatural confrontation.

---

## 🎮 Core Features & Gameplay Mechanics

### 1. Interactive Carriage Exploration & Point-and-Click Hotspots
Navigate through Carriages 1 to 6 using detailed maps and interactive hotspots to inspect items, open cabin doors, examine crime scenes, and find hidden golden tickets.

### 2. Time-Loop Investigation ("Every Day Changing It")
Each time loop resets the train with subtle and dramatic differences:
- Altered environment conditions, creepy lighting, and entity shadows.
- Dynamic dialogue states and new questioning options based on previously discovered clues.
- Changing evidence and clue locations across loop iterations.

### 3. Minigames & Casino Systems
- **Mahjong Tile Matching:** Test your observation and tile-matching skills in Carriage 2.
- **Slot Machine & Coin Arcade:** Earn and bet arcade coins to win golden tickets (`game/slots.rpy`).
- **Flashlight & Horror Navigation:** Use flashlight mechanics and dark vision shaders during empty train sequence explorations (`game/empty_train.rpy`).

### 4. Audio & In-Game Radio Bar
- Full atmospheric soundtrack featuring ambient themes, tension tracks, and retro radio songs (*Tears For Fears*, *Tame Impala*, *Rockwell*, etc.).
- On-screen Interactive Radio Bar (`Settings > Audio > Radio Bar`) accessible during gameplay.

### 5. Secret Achievements & EXTRAS > 4:01
Unlock special notes and achievements (`game/secrets.rpy`) by discovering hidden secrets:
- **Konami Code:** Input code sequences for hidden easter eggs.
- **Cast Call:** Type character names on the main menu.
- **Logo Poking:** Interact repeatedly with the Blackberry Studios logo.
- **Time Check:** Launch or visit the main menu at exactly 4:00 AM/PM.
- **Hanyu Interaction:** Pet Hanyu in the credits screen.
- **Golden Ticket Hunt:** Find all hidden golden tickets scattered across the train.

---

## 🎮 Game Controls

| Input | Action |
| --- | --- |
| **Left Click / Space / Enter** | Advance dialogue / Select choices / Interact with hotspots |
| **Escape / Right Click** | Open Game Menu (Save, Load, Preferences, Extras, Quit) |
| **Ctrl (Hold)** | Fast forward / Skip seen text |
| **Tab** | Toggle dialogue skipping mode |
| **Mouse Wheel** | Scroll up/down to review dialogue history log |

---

## 👥 Character Directory

| Character | Role / Description |
| --- | --- |
| **Louis** | Main protagonist; trapped investigator seeking a way home |
| **Dorothy** | Train conductor on the Grekhov Express keeping order |
| **Fedora** | Lead journalist from *The Owlfeather* searching for her big scoop |
| **Eduard** | Carriage 2 bartender who knows everyone's secrets and tab history |
| **Jackie** | Attentive carriage staff member cleaning up crime scene glass |
| **Shunyu** | High-stakes Mahjong gambler; victim of the train murder |
| **Kimmy** | Wealthy clock business heiress traveling in the luxury suite |
| **Himmel** | Kimmy's nervous husband hiding a secret dependence on banned substances |
| **Sebastian** | Strict butler guarding Misha and family secrets |
| **Misha** | Quiet child playing with blocks in the sleeper cabin; a key suspect |
| **Agatha** | Pragmatic assistant nurse staffing the medical cart |
| **Ichora** | Train engineer holding critical access keys |
| **Pattison** | Cryptic mailroom worker sorting letters and muttering rhymes |
| **Alexander** | Storage cart merchant dealing in contraband maple sugar |
| **Supernatural Entities** | Horrors waiting in Carriage 6 (The Passenger, The Gentleman, The Conductor) |

---

## 💻 System Specifications

| Component | Minimum Requirement | Recommended |
| --- | --- | --- |
| **OS** | 64-bit Windows 10, macOS 11+, or 64-bit Linux | Windows 11 / macOS 13+ / Linux |
| **Processor** | Dual-core CPU ~2.0 GHz | Quad-core CPU ~3.0 GHz+ |
| **Memory (RAM)** | 4 GB RAM | 8 GB RAM |
| **Graphics** | Integrated GPU with OpenGL 2.0 or DirectX 11 | Dedicated GPU / Apple Silicon |
| **Storage** | 300 MB available space | 300 MB available space |
| **Display** | 1280×720 minimum | **1920×1080** (Native Resolution) |

---

## 🚀 Running the Game & Development Guide

### Launching via Ren'Py SDK (Source)
1. Install [Ren'Py SDK 8.0+](https://www.renpy.org/).
2. Clone this repository into your Ren'Py projects directory.
3. Open Ren'Py SDK and select **"Add Existing Project"**.
4. Choose the repository directory (project name: `Working`) and click **"Launch Project"**.

### Asset Generation Tools
The repository includes automated asset generation Python scripts in `tools/`:
- **UI Assets:** `python3 tools/gen_ui_assets.py game/gui` (Generates rounded mask templates and key string assets)
- **Horror Assets:** `python3 tools/gen_horror_assets.py game` (Generates audio stings, static sound effects, vignette overlays, and flashlight masks)

---

## 🛠️ Development Team & Credits

**Studio:** Blackberry Studios
**Engine:** Ren'Py (Python)

- **Direction & Design:** Eric Zheng
- **Programming & Scripting:** Eric Zheng, Ryan
- **Lead Graphic Designers:** Hannah, Aydin
- **Story & Writing:** Hannah
- **Character Design:** Hannah, Aydin
- **Map & Carriage Design:** Aydin
- **R&D & Technical Support:** Eric Zheng
- **Financial & Budget Director:** Eric Zheng

---

## 📜 License

- Powered by the [Ren'Py Visual Novel Engine](https://www.renpy.org/).
- © Blackberry Studios. All rights reserved.
