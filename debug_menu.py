import sys
import os

# Force Python to look in current folder first
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
import ui.menu

print("menu.py path being used:", ui.menu.__file__)

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Create MainMenu instance
menu = ui.menu.MainMenu(screen)

# List all attributes
print("\nAll attributes of menu object:")
for attr in dir(menu):
    print(attr)

# Check if option_font exists
if hasattr(menu, "option_font"):
    print("\n✅ option_font exists!")
else:
    print("\n❌ option_font does NOT exist!")

pygame.quit()