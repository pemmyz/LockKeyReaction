# 🔒 LockKeyReaction

**LockKeyReaction** is a reflex-testing game that uses your keyboard’s lock LEDs (Caps Lock, Num Lock, Scroll Lock) as visual prompts! Hit the correct key in time, and the game speeds up — miss it, and you'll have to keep up!

Originally designed for Linux using `xdotool` and `xset`, this version also includes on-screen status lights so it should work on Windows (currently not supported) and non-LED setups too. ⌨️✨

---

## 🧠 Idea Behind the Game

This game started as a fun way to test reflexes using actual **keyboard LED lights**.
It evolved into a fully-featured **Python + Pygame** application with real-time stats and cross-platform (Windows currently not supported) support.

This idea is probably as old as the first keyboards that came with lock key lights — and the ability to programmatically toggle them.
I wasn’t the first person to come up with this idea — and the person I originally heard it from probably wasn’t the first either. This is just my take on a fun concept that’s been floating around in different forms. 

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
```
bash
sudo apt install xdotool
pip install pygame 
```

---

## 🚀 Run It

```bash
python lockkeyreactionmain.py
```

## To be added
Adjust the logic, make it so that the reactiontime balances around players ability to hit keys, too slow and game will slow down and too fast and game will pick up the pace. And depending on the players ability to hit correct key in time will give scores and game will have different durations games and highscore list. Adjust the game so it will work on other operating systems like Windows. Now there might be things coded that are not crossplatform.



## 🧠 Game Logic Update Plan

- The game will **adapt its reaction time** dynamically based on the player's key press performance:
  - If the player consistently presses keys **too slowly**, the game will slow down to stay challenging but fair.
  - If the player hits keys **very quickly and accurately**, the game will **speed up** to increase the difficulty.

## 🎯 Scoring System

- Score will be based on:
  - Hitting the correct key in time.
  - Reaction accuracy (how fast you hit the key after prompt).
- Missed or incorrect keys will reduce the score or combo.

## ⏱️ Game Duration & Variants

- Multiple game duration options (e.g., 30s, 60s, endless mode).
- The high score list will reflect top performances based on selected durations.

## 🌐 Cross-Platform Compatibility

- Adjustments will be made to ensure full support on **Windows**, **Linux**, and **macOS**.
- Code will be refactored to remove or replace platform-specific functionality with **cross-platform alternatives**:
  - Avoid hardcoded paths or OS-specific calls.
  - Use standard Python libraries and OS-independent file handling where possible.

## 💾 Highscore System

- Persistent highscore list stored in a simple JSON or text file.
- Optionally support per-duration leaderboards.

## 🚧 TODO

- [ ] Implement dynamic reaction time scaling.
- [ ] Add scoring and combo system.
- [ ] Build game duration options.
- [ ] Implement cross-platform input handling.
- [ ] Create and store highscore lists.

Stay tuned for updates!
