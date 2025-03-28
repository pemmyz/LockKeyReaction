# 🔒 LockKeyReaction

**LockKeyReaction** is a reflex-testing game that uses your keyboard’s lock LEDs (Caps Lock, Num Lock, Scroll Lock) as visual prompts! Hit the correct key in time, and the game speeds up — miss it, and you'll have to keep up!

Originally designed for Linux using `xdotool` and `xset`, this version also includes on-screen status lights so it should work on Windows and non-LED setups too. ⌨️✨

---

## 🎮 Gameplay

- **LEDs will light up randomly** (or status prompts will appear).
- You must press the **correct key** before the time runs out:
  - `Num Lock` → ← Left arrow
  - `Caps Lock` → ↓ Down arrow
  - `Scroll Lock` → → Right arrow
- The game gets faster the better you do!
- View **real-time stats** like:
  - Accuracy, reaction times, streaks, median, percentiles, and more.

---


## 📊 Stats Tracked

- Fastest / Slowest / Average reaction time  
- Median, Standard Deviation  
- 25th and 75th Percentiles  
- Missed prompts  
- Accuracy & Prompt ratio  
- Current and longest streaks  
- Total game time & unpaused time  

## 🛠️ Requirements

### Linux:
- Python 3
- [Pygame](https://www.pygame.org/)
- `xdotool`
- `xset`

Install requirements:

bash
sudo apt install xdotool
pip install pygame 


---


