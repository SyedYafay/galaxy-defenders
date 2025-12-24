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

INTRO, MENU, GAME, OPTIONS, CREDITS = "intro", "menu", "game", "options", "credits"
state = INTRO

# ================= INTRO =================
intro_font = pygame.font.SysFont("arial", 72, bold=True)
intro_alpha = 0
intro_timer = 120
intro_fade_in = True
intro_fade_out = False

# ================= MENU =================
menu = MainMenu(screen)

# Arrow aligned to menu text
ARROW_X = WIDTH // 2 - 260
ARROW_OFFSET_Y = 8   # FIXED ALIGNMENT

# ================= GAME =================
game_scene = GameScene(screen)

# ================= BACKGROUND =================
bg_image = pygame.image.load("assets/images/menu_bg.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# ================= MUSIC =================
music_path = "assets/music/menu.wav"

# ================= SFX =================
menu_move_sfx = pygame.mixer.Sound("assets/sounds/menu_move.wav")
menu_move_sfx.set_volume(0.5)

# ================= FADE =================
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))
fade_alpha = 0
fade_speed = 12
fading_out = False
fading_in = False

# ================= OPTIONS =================
volume = 0.4
font = pygame.font.SysFont("arial", 38)
big_font = pygame.font.SysFont("arial", 70, bold=True)

running = True
while running:
    clock.tick(60)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # ---------- MENU INPUT ----------
        if state == MENU and event.type == pygame.KEYDOWN:
            old = menu.selected
            if event.key == pygame.K_UP:
                menu.move_up()
                if old != menu.selected:
                    menu_move_sfx.play()
            elif event.key == pygame.K_DOWN:
                menu.move_down()
                if old != menu.selected:
                    menu_move_sfx.play()
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
            elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                state = MENU
            pygame.mixer.music.set_volume(volume)
            menu_move_sfx.set_volume(volume)

        elif state == CREDITS and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                state = MENU

    # ================= INTRO =================
    if state == INTRO:
        screen.fill((0, 0, 0))
        txt = intro_font.render("A Game by Cosmic Forge", True, (210, 210, 255))
        txt.set_alpha(intro_alpha)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))

        if intro_fade_in:
            intro_alpha += 4
            if intro_alpha >= 255:
                intro_fade_in = False
        else:
            intro_timer -= 1
            if intro_timer <= 0:
                intro_fade_out = True

        if intro_fade_out:
            intro_alpha -= 6
            if intro_alpha <= 0:
                state = MENU
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)

        pygame.display.update()
        continue

    # ================= FADE =================
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

    # ================= UPDATE =================
    if state == GAME:
        result = game_scene.handle_input(events)
        if result == "menu":
            state = MENU
        game_scene.update()

    # ================= DRAW =================
    screen.blit(bg_image, (0, 0))

    if state == MENU:
        menu.draw()
        option_y = menu.get_selected_y()
        arrow_y = option_y + ARROW_OFFSET_Y
        pygame.draw.polygon(
            screen, (0, 255, 255),
            [(ARROW_X, arrow_y),
             (ARROW_X + 20, arrow_y + 10),
             (ARROW_X, arrow_y + 20)]
        )

    elif state == OPTIONS:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        screen.blit(big_font.render("OPTIONS", True, (255,255,255)), (WIDTH//2 - 120, 150))
        screen.blit(font.render("VOLUME", True, (200,200,200)), (WIDTH//2 - 70, 300))
        pygame.draw.rect(screen, (100,100,100), (WIDTH//2 - 150, 350, 300, 10))
        pygame.draw.circle(screen, (0,255,255),
                           (WIDTH//2 - 150 + int(volume*300), 355), 12)

    elif state == CREDITS:
        screen.fill((0,0,0))
        start_y = 60
        spacing = 32
        for i, line in enumerate([
            "GALAXY DEFENDERS","",
            "Game Design & Programming","Yafay","",
            "UI / UX Design","Yafay","",
            "Sound Effects","Yafay","",
            "Testers","Aliza","Rafey","Dua","",
            "Special Thanks","ChatGPT","Nescafé ☕"
        ]):
            txt = font.render(line, True, (200,200,200))
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, start_y + i*spacing)))

    elif state == GAME:
        game_scene.draw()

    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

    pygame.display.update()

pygame.quit()
