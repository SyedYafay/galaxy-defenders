import pygame
import os

from ui.menu import MainMenu
from ui.game import GameScene

# ================= INIT =================
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1300, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Defenders")
clock = pygame.time.Clock()

# ================= STATES =================
MENU = "menu"
GAME = "game"
state = MENU

# ================= MENU =================
menu = MainMenu(screen)

# ---------- ARROW ----------
ARROW_X = WIDTH // 2 - 220
ARROW_START_Y = int(HEIGHT * 0.35)
ARROW_SPACING = 70
ARROW_SIZE = 20

# ================= GAME =================
game_scene = GameScene(screen)

# ================= BACKGROUND =================
bg_image = None
bg_path = os.path.join("assets", "images", "menu_bg.jpg")
if os.path.exists(bg_path):
    bg_image = pygame.image.load(bg_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# ================= MUSIC =================
music_path = os.path.join("assets", "music", "menu.wav")
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

# ================= SFX (ONLY MOVE — LIKE YOU HAD) =================
menu_move_sfx = None
move_path = os.path.join("assets", "sounds", "menu_move.wav")
if os.path.exists(move_path):
    menu_move_sfx = pygame.mixer.Sound(move_path)
    menu_move_sfx.set_volume(0.5)

# ================= FADE =================
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))
fade_alpha = 0
fade_speed = 12
fading_out = False
fading_in = False

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(60)
    events = pygame.event.get()

    # ---------- EVENTS ----------
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # ===== MENU INPUT =====
        if state == MENU and event.type == pygame.KEYDOWN:
            old = menu.selected

            if event.key == pygame.K_UP:
                menu.move_up()
                if old != menu.selected and menu_move_sfx:
                    menu_move_sfx.play()

            elif event.key == pygame.K_DOWN:
                menu.move_down()
                if old != menu.selected and menu_move_sfx:
                    menu_move_sfx.play()

            elif event.key == pygame.K_RETURN:
                # START GAME
                if menu.selected == 0 and not fading_out and not fading_in:
                    fade_alpha = 0
                    fading_out = True

                # QUIT
                elif menu.selected == 3:
                    running = False

    # ---------- FADE LOGIC ----------
    if fading_out:
        fade_alpha += fade_speed
        if fade_alpha >= 255:
            fade_alpha = 255
            fading_out = False
            state = GAME
            game_scene = GameScene(screen)
            fading_in = True

    if fading_in:
        fade_alpha -= fade_speed
        if fade_alpha <= 0:
            fade_alpha = 0
            fading_in = False

    # ---------- UPDATE ----------
    if state == GAME:
        result = game_scene.handle_input(events)
        if result == "menu":
            state = MENU
        game_scene.update()

    # ---------- DRAW ----------
    if state == MENU:
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((10, 20, 40))

        menu.draw()

        # ===== DRAW ARROW =====
        arrow_y = ARROW_START_Y + menu.selected * ARROW_SPACING + ARROW_SIZE // 2
        pygame.draw.polygon(
            screen,
            (0, 255, 255),
            [
                (ARROW_X, arrow_y),
                (ARROW_X + ARROW_SIZE, arrow_y + ARROW_SIZE // 2),
                (ARROW_X, arrow_y + ARROW_SIZE),
            ]
        )

    elif state == GAME:
        game_scene.draw()

    # ---------- FADE OVERLAY ----------
    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

    pygame.display.update()

pygame.quit()
 