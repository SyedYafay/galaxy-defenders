import pygame
from ui.menu import MainMenu

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/music/menu.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 1300, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga Retro")

clock = pygame.time.Clock()
menu = MainMenu(screen)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu.move_up()
            elif event.key == pygame.K_DOWN:
                menu.move_down()
            elif event.key == pygame.K_RETURN:
                choice = menu.select()
                if choice == "Play":
                    screen.fill((0, 100, 0))
                    play_font = pygame.font.SysFont("arial", 60, bold=True)
                    play_text = play_font.render("PLAY SELECTED", True, (255, 255, 255))
                    screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2 - play_text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(1000)
                elif choice == "Options":
                    screen.fill((50, 0, 50))
                    opt_font = pygame.font.SysFont("arial", 60, bold=True)
                    opt_text = opt_font.render("OPTIONS SELECTED", True, (255, 255, 255))
                    screen.blit(opt_text, (WIDTH//2 - opt_text.get_width()//2, HEIGHT//2 - opt_text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(1000)
                elif choice == "Credits":
                    screen.fill((0, 0, 100))
                    cred_font = pygame.font.SysFont("arial", 60, bold=True)
                    cred_text = cred_font.render("CREDITS SELECTED", True, (255, 255, 255))
                    screen.blit(cred_text, (WIDTH//2 - cred_text.get_width()//2, HEIGHT//2 - cred_text.get_height()//2))
                    pygame.display.update()
                    pygame.time.delay(1000)
                elif choice == "Exit":
                    running = False

    menu.draw()
    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()
