import pygame
import os

from ui.menu import MainMenu
from ui.game import GameScene

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1300, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Defenders")
clock = pygame.time.Clock()

MENU = "menu"
GAME = "game"
OPTIONS = "options"
CREDITS = "credits"
state = MENU

menu = MainMenu(screen)

ARROW_X = WIDTH // 2 - 220
ARROW_START_Y = int(HEIGHT * 0.35)
ARROW_SPACING = 70
ARROW_SIZE = 20

game_scene = GameScene(screen)

bg_image = None
bg_path = os.path.join("assets", "images", "menu_bg.jpg")
if os.path.exists(bg_path):
    bg_image = pygame.image.load(bg_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

music_path = os.path.join("assets", "music", "menu.wav")
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

menu_move_sfx = pygame.mixer.Sound(os.path.join("assets", "sounds", "menu_move.wav"))
menu_move_sfx.set_volume(0.5)

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))
fade_alpha = 0
fade_speed = 12
fading_out = False
fading_in = False

volume = 0.4
font = pygame.font.SysFont("arial", 40)
big_font = pygame.font.SysFont("arial", 70, bold=True)

running = True
while running:
    clock.tick(60)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if state == MENU and event.type == pygame.KEYDOWN:
            old = menu.selected
            if event.key == pygame.K_UP:
                menu.move_up()
                if old != menu.selected: menu_move_sfx.play()
            elif event.key == pygame.K_DOWN:
                menu.move_down()
                if old != menu.selected: menu_move_sfx.play()
            elif event.key == pygame.K_RETURN:
                if menu.selected == 0:
                    fading_out = True
                elif menu.selected == 1:
                    state = OPTIONS
                elif menu.selected == 2:
                    state = CREDITS
                elif menu.selected == 3:
                    running = False

        elif state == OPTIONS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                volume = max(0, volume - 0.05)
            elif event.key == pygame.K_RIGHT:
                volume = min(1, volume + 0.05)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                state = MENU
            pygame.mixer.music.set_volume(volume)
            menu_move_sfx.set_volume(volume)

        elif state == CREDITS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                state = MENU

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

    if state == GAME:
        result = game_scene.handle_input(events)
        if result == "menu":
            state = MENU
        game_scene.update()

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((10, 20, 40))

    if state == MENU:
        menu.draw()
        arrow_y = ARROW_START_Y + menu.selected * ARROW_SPACING + ARROW_SIZE // 2
        pygame.draw.polygon(screen, (0,255,255), [
            (ARROW_X, arrow_y),
            (ARROW_X + ARROW_SIZE, arrow_y + ARROW_SIZE//2),
            (ARROW_X, arrow_y + ARROW_SIZE)
        ])

    elif state == OPTIONS:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        screen.blit(overlay, (0,0))
        screen.blit(big_font.render("OPTIONS", True, (255,255,255)), (WIDTH//2-120, 150))
        screen.blit(font.render("VOLUME", True, (200,200,200)), (WIDTH//2-70, 300))
        pygame.draw.rect(screen, (100,100,100), (WIDTH//2-150, 350, 300, 10))
        pygame.draw.circle(screen, (0,255,255), (WIDTH//2-150 + int(volume*300), 355), 12)

    elif state == CREDITS:
        screen.fill((0,0,0))
        lines = [
            "GALAXY DEFENDERS",
            "",
            "Game Design & Programming",
            "Yafay",
            "",
            "UI / UX Design",
            "Yafay",
            "",
            "Sound Effects",
            "Yafay",
            "",
            "Special Thanks",
            "ChatGPT",
            "Nescafé ☕",
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, (200,200,200))
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, 120+i*35)))

    elif state == GAME:
        game_scene.draw()

    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

    pygame.display.update()

pygame.quit()
