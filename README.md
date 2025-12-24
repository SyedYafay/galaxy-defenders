🚀 Galaxy Defenders

Galaxy Defenders is a retro-inspired 2D space shooter built using Python and Pygame, inspired by classic arcade games like Galaga.
The project features structured game states, smooth UI transitions, sound effects, wave-based enemy progression, and persistent high scores.

This project was developed as part of my learning journey in Computer Science, focusing on game loops, state management, and user experience design.

🎮 Game Overview

You control a space ship defending the galaxy against waves of alien invaders.
Each wave increases in difficulty, featuring more enemies and stronger aliens.
Survive as long as possible, score points, and beat your high score.

🧭 Main Menu Features

The main menu is fully interactive and includes:

▶ START GAME

Begins the game with a smooth fade transition

Loads Wave 1 with a countdown-style delay

⚙ OPTIONS

Opens a black translucent overlay

Adjustable volume slider

Controls background music

Controls sound effects

Controlled using Left / Right Arrow keys

Press ESC or ENTER to return to menu
❌ QUIT

Exits the game safely

🕹 Gameplay Features
🚀 Player Controls

Left Arrow / Right Arrow → Move ship

Spacebar → Shoot

ESC → Pause game

👾 Enemies & Waves

Enemies spawn in properly aligned grids across the full screen

Two enemy types:

Normal aliens (1 HP)

Strong aliens (2 HP)

Enemies shoot back at random intervals

Waves scale progressively

🌊 Wave System

Displays WAVE 1, WAVE 2, WAVE 3…

Each wave begins with:

Player centered

Enemies frozen

2-second delay before action starts

Creates a classic arcade “get ready” illusion

⏸ Pause Menu

Press ESC to pause

Options:

Resume

Return to Main Menu

Navigation via Arrow keys + ENTER

💀 Game Over Screen

Displays GAME OVER

Shows instruction:

Press ENTER to return to Main Menu

Prevents resuming the game

Lives never go negative

🏆 Score & High Score System

Score increases when enemies are destroyed

High score is saved locally (highscore.txt)

High score is displayed below current score

Automatically updates if a new high score is achieved

🔊 Audio Features

Background menu music

Menu navigation sound effects

Shooting sound (shoot.wav)

Volume fully adjustable via Options menu
🧰 Requirements to Run
📌 Software Requirements

Python 3.9+

Pygame

📦 Install Dependencies
pip install pygame

▶ How to Run the Game

From the project root directory:

python main.py

🧠 Learning Outcomes

This project demonstrates:

Game state management

Event handling

UI/UX design in Pygame

File I/O (high score saving)

Audio integration

Clean project structure

Incremental feature development

🙌 Credits

Developed by Yafay
Special thanks to ChatGPT for guidance and Nescafé for fuel ☕