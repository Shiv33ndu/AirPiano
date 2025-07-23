# 🎹 Air Piano (2 Octave Virtual Piano with Hand Tracking)

Play music *in the air* with no physical keys — just your hands, your webcam, and your browser.

![air-piano-demo](demo.gif) <!-- Optional: Add demo GIF if available -->

## ✨ Features

- 👋 **Touchless piano** using real-time hand tracking (MediaPipe Hands)  
- 🎯 **Accurate key presses** based on finger joint angles (tip below pip)  
- 🔄 **Circular piano layout** for aesthetic UI & two-octave coverage  
- 🔊 **Volume control** by waving your **right hand up/down**  
- 👁️ **Multi-hand support** with real-time visual feedback  
- 🔈 Powered by **Pygame sound engine** for smooth audio playback  

---

## 🧠 Tech Stack

| Technology     | Role                           |
|----------------|--------------------------------|
| **OpenCV**     | Video frame capture + UI       |
| **MediaPipe**  | Hand landmark detection        |
| **Pygame**     | Sound playback engine          |
| **Python**     | Core logic & integration       |

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8+
- pip

### 🔧 Installation

```bash
git clone https://github.com/<your-username>/air-piano.git
cd air-piano
pip install -r requirements.txt
```

### ▶️ Run the App

```bash
python air_piano.py
```

---

## 🎛️ Controls

| Action              | How to do it                                      |
|---------------------|--------------------------------------------------|
| Play a note         | Move a fingertip **into** and press **down** on a circular key |
| Volume control      | Move your **right hand** up/down in the frame (little bugged)   |
| Visual feedback     | Green circle when finger presses a key (wokring on it)           |
| Multi-hand playing  | Use **both hands** to play chords in real time(working on it)   |

---

## 📁 Project Structure

```
air-piano/
│
├── air_piano.py           # Main file: draws UI, plays sound, detects presses
├── hand_detector.py       # Class-based wrapper for MediaPipe Hands
├── sounds/                # Folder with all .wav files for 2 octaves
├── assets/                # (Optional) Visual assets or UI overlays
├── README.md              # You're reading it!
└── requirements.txt       # All Python dependencies
```

---

## 🎯 Future Improvements

- 🖐️ Gesture-based scale selection or sustain  
- 🎹 Switch between piano/synth sounds  
- 📱 Mobile support via webcam server  
- 💾 Record played notes as MIDI file  

---

## 🙌 Credits

- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands)  
- [Pygame](https://www.pygame.org/docs/)  
- Inspiration from gesture-controlled musical instruments  

---

## 📸 Demo

> Incoming!

---

## 🪄 License

MIT License — free to use, remix, and enhance with credits. 🎶
