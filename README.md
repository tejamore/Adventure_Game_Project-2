# Adventure Game Project

This repository contains a text-based adventure game built in Python as a course-end project.

Files added:
- adventure_game.py : Main game script
- requirements.txt : Python dependencies
- REPORT.md : Short report you can convert to PDF

How to run

1. (Optional) Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows

2. Install dependencies:
   pip install -r requirements.txt

3. Run the game:
   python adventure_game.py

Notes on cinematic effects and sound
- The script uses ASCII art, slow_print timing, and colors (via colorama) to create a cinematic CLI feel.
- Sounds are optional. If you want sound effects, add WAV/MP3 files into `assets/sounds/`:
  - intro.wav (intro music)
  - torch.wav (torch lighting)
  - treasure.wav (victory sound)

The script will try to use playsound if installed. If not, the game runs without sound.

Contributing
- You're welcome to enhance the story, visuals, and add audio assets. Submit pull requests.
