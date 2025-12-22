# Galaxy Defenders

A Pygame-based 2D space shooter game inspired by Galaga. Currently in early development with a fully functional menu system.

## Features

- **Main Menu System**: Navigate through game options with keyboard controls
- **Background Music**: Atmospheric menu music with volume control
- **Sound Effects**: Menu navigation and selection sound effects
- **Visual Design**: Custom background image and styled menu interface
- **Menu Options**: Play, Options, Credits, and Exit

## Prerequisites

- **macOS** (tested on macOS)
- **Python 3.6+** (Python 3.x required)
- **pip** (Python package installer)

## Installation

### Step 1: Check Python Installation

First, verify that Python 3 is installed on your MacBook:

```bash
python3 --version
```

You should see output like `Python 3.x.x`. If Python 3 is not installed, download it from [python.org](https://www.python.org/downloads/) or install via Homebrew:

```bash
brew install python3
```

### Step 2: Install Pygame

Install the pygame library using pip:

```bash
pip3 install pygame
```

If you encounter permission issues, you may need to use:

```bash
pip3 install --user pygame
```

Or use a virtual environment (recommended):

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install pygame
pip install pygame
```

### Step 3: Verify Assets

Ensure the following assets are present in the project:

- `assets/images/menu_bg.jpg` - Menu background image
- `assets/music/menu.wav` - Menu background music
- `assets/sounds/menu_move.wav` - Menu navigation sound effect

The game will run without these assets, but you'll see warning messages in the console.

## Running the Game

Navigate to the project directory and run:

```bash
python3 main.py
```

Or if you're using a virtual environment:

```bash
source venv/bin/activate
python main.py
```

The game window will open at **1300x680 pixels** resolution.

## Controls

- **↑ (Up Arrow)**: Move selection up
- **↓ (Down Arrow)**: Move selection down
- **Enter/Return**: Select menu option
- **Close Window**: Exit the game

## Project Structure

```
Galaxy-Defenders/
├── main.py              # Main entry point and game loop
├── debug_menu.py        # Debug script for menu testing
├── ui/
│   ├── __init__.py
│   └── menu.py          # MainMenu class implementation
└── assets/
    ├── images/
    │   └── menu_bg.jpg
    ├── music/
    │   └── menu.wav
    └── sounds/
        └── menu_move.wav
```

## Current Status

The project currently implements:
- ✅ Main menu system with navigation
- ✅ Background music and sound effects
- ✅ Visual menu interface with highlighting

**In Development** (as noted in code TODOs):
- ⏳ Game scene/play mode
- ⏳ Options menu
- ⏳ Credits screen

## Troubleshooting

### Python Command Not Found
If `python3` command is not found, ensure Python 3 is installed and in your PATH. You can check with:
```bash
which python3
```

### Pygame Installation Issues
If pygame fails to install, try:
```bash
pip3 install --upgrade pip
pip3 install pygame
```

### Missing Assets Warning
If you see warnings about missing assets, ensure the `assets/` directory structure matches the expected layout above.

### Audio Issues
If you don't hear music or sound effects:
- Check your system volume
- Verify the audio files exist in the `assets/` directory
- Check console output for error messages

## Development Notes

- The game runs at 60 FPS (frames per second)
- Menu music loops continuously (`-1` parameter)
- Sound effect volumes are set to 0.5 (50%)
- Background music volume is set to 0.4 (40%)

## License

[Add your license information here]

