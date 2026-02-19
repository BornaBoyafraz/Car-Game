# 🚗 Car Game

A 2D lane-based car dodging arcade game built with Python and Pygame.  
The player switches between three lanes to avoid incoming traffic and keep the run alive.  
Game speed increases every 5 points, with score tracking, high score tracking, crash detection, sound effects, and restart flow.

![Gameplay Preview](Car_gif.gif)

## 🎮 Gameplay Features

- Lane-based movement across three fixed road lanes
- Random incoming vehicles as obstacles
- Score counter and high score tracking during the session
- Progressive difficulty (speed increases every 5 points)
- Collision detection with crash visual + sound effect
- Start, pause, game-over, and restart states

## ⚙️ Technical Highlights

- Object-oriented structure using `Vehicle` and `PlayerVehicle` classes
- Pygame sprite groups for entity management and rendering
- Sprite collision handling for game-over triggers
- Real-time game loop with update/draw/event phases
- HUD rendering for score, high score, level, and FPS

## 🧱 Built With

- Python 3
- Pygame

## 📁 Project Structure

```text
Car Game/
├── Car Game.py
├── Images/
│   ├── car.png
│   ├── crash.png
│   ├── pickup_truck.png
│   ├── semi_trailer.png
│   ├── taxi.png
│   └── van.png
├── point.mp3
├── Crash.mp3
├── Car_gif.gif
└── README.md
```

## 🚀 Installation & How to Run

```bash
# 1) Clone the repository
git clone https://github.com/BornaBoyafraz/<your-repo-name>.git

# 2) Enter the project folder
cd <your-repo-name>

# 3) Install dependencies
pip install pygame

# 4) Run the game
python "Car Game.py"
```

## ⌨️ Controls

- `SPACE`: Start game / Restart after crash
- `A` or `←`: Move left
- `D` or `→`: Move right
- `P`: Pause / Resume
- `Q` or `ESC`: Quit

## 🔮 Future Improvements

- Persistent high score saving to file
- Main menu and settings screen
- Multiple game modes and difficulty presets
- Additional vehicle patterns and lane behavior
- Improved game-over transition and feedback polish

## 🧠 Why I Built This

This project was built to demonstrate practical core game-programming skills:

- Object-Oriented Programming
- Sprite groups and collision handling
- Game loop structure
- Increasing difficulty systems
- UI/HUD implementation

## 👨‍💻 About the Developer

**Seyedborna Boyafraz**  
Website: [bornaba.com](https://www.bornaba.com/)  
GitHub: [@BornaBoyafraz](https://github.com/BornaBoyafraz)

