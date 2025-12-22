import pygame
from ui.menu import MainMenu
import os

# ---------------- INIT ----------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1300, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Defenders")

clock = pygame.time.Clock()

# ---------------- MUSIC ----------------
music_path = os.path.join("assets", "music", "menu.wav")
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
else:
    print("Menu music missing!")

# ---------------- SFX ----------------
move_sfx_path = os.path.join("assets", "sounds", "menu_move.wav")
select_sfx_path = os.path.join("assets", "sounds", "menu_select.wav")

menu_move_sfx = pygame.mixer.Sound(move_sfx_path) if os.path.exists(move_sfx_path) else None
menu_select_sfx = pygame.mixer.Sound(select_sfx_path) if os.path.exists(select_sfx_path) else None

if menu_move_sfx: menu_move_sfx.set_volume(0.5)
if menu_select_sfx: menu_select_sfx.set_volume(0.5)

# ---------------- MENU ----------------
menu = MainMenu(screen)

# ---------------- ARROW ----------------
ARROW_X = WIDTH // 2 - 150
ARROW_START_Y = int(HEIGHT * 0.35)
ARROW_SPACING = 70
ARROW_SIZE = 20  # triangle width/height

# ---------------- LOOP ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                old = menu.selected
                menu.move_up()
                if menu.selected != old and menu_move_sfx:
                    menu_move_sfx.play()

            if event.key == pygame.K_DOWN:
                old = menu.selected
                menu.move_down()
                if menu.selected != old and menu_move_sfx:
                    menu_move_sfx.play()

            if event.key == pygame.K_RETURN:
                if menu_select_sfx:
                    menu_select_sfx.play()
                selected = menu.selected

                if selected == 0:  # Play
                    print("START GAME")  # TODO: switch to game scene
                elif selected == 1:  # Options
                    print("OPTIONS")    # TODO: show options menu
                elif selected == 2:  # Credits
                    print("CREDITS")    # TODO: show credits screen
                elif selected == 3:  # Exit
                    running = False

    # ---------------- DRAW ----------------
    menu.draw()

    # Draw triangle arrow
    arrow_y = ARROW_START_Y + menu.selected * ARROW_SPACING
    pygame.draw.polygon(
        screen,
        (0, 255, 255),
        [
            (ARROW_X, arrow_y),
            (ARROW_X + ARROW_SIZE, arrow_y + ARROW_SIZE // 2),
            (ARROW_X, arrow_y + ARROW_SIZE),
        ]
    )

    pygame.display.update()

pygame.quit()
