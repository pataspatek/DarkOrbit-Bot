# 🚀 Dark Orbit Bot (Python Automation)

A **real-time automation bot** for the browser game **Dark Orbit**.  
This bot captures the game window, detects loot boxes, and automatically collects them — simulating human-like clicks and movement across the map.

> ⚠️ **Disclaimer:** This project is intended **for educational and research purposes only.**  
> Automating gameplay in online games may violate their Terms of Service.

---

## 🧠 Features

- 🪞 **Real-time Screen Capture** — Captures the game window directly using Win32 API (for maximum FPS).  
- 🎯 **Loot Box Detection** — Uses OpenCV and NumPy to locate loot boxes on screen.  
- 🕹️ **Auto-Clicking & Navigation** — Simulates user input via PyAutoGUI to click loot and move the ship.  
- ⚙️ **Threaded Processing** — Uses Python threading with locks to handle capture, detection, and clicking simultaneously.  
- 🧩 **Human-like Behavior** — Randomized timings and movements for natural interaction.

---

## 🧰 Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.x** | Core programming language |
| **OpenCV (cv2)** | Image processing and detection |
| **NumPy** | Matrix and pixel manipulation |
| **pyautogui** | Simulated mouse and keyboard control |
| **win32gui / win32ui / win32con** | Efficient Windows screen capture |
| **threading / Lock** | Multithreading control and concurrency safety |
| **time / random** | Timing and human-like randomness |

---

## ▶️ Usage

1. Open **Dark Orbit** and set your screen so the game window is visible.  
2. Adjust the window name in `window_capture.py` if needed (e.g., `"DarkOrbit"`).  
3. Run the main bot script:
   ```bash
   python main.py
4. The bot will:
   - Capture the game screen in real time
   - Detect loot boxes
   - Click on them automatically
   - Move your ship to the next location on the map

---

## 🧑‍💻 Author

**Patrik Pátek**
🐙 [GitHub](https://github.com/pataspatek)


