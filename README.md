# 🔒 LockKeyReaction

**LockKeyReaction** is a reflex-testing game that uses your keyboard’s lock LEDs (Caps Lock, Num Lock, Scroll Lock) as visual prompts! Hit the correct key in time, and the game speeds up — miss it, and you'll have to keep up!

Originally designed for Linux using `xdotool` and `xset`, this version also includes on-screen status lights so it should work on Windows and non-LED setups too. ⌨️✨

---

## 🧠 Idea Behind the Game

This game started as a fun way to test reflexes using actual **keyboard LED lights**.
It evolved into a fully-featured **Python + Pygame** application with real-time stats and cross-platform support.

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

