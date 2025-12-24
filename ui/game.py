import pygame
import random
import os

HIGHSCORE_FILE = "highscore.txt"

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        self.PLAYING = "playing"
        self.PAUSED = "paused"
        self.GAMEOVER = "gameover"
        self.WAVE_DELAY = "wave_delay"
        self.state = self.WAVE_DELAY

        self.player_img = pygame.transform.scale(
            pygame.image.load("assets/images/ship1.png").convert_alpha(), (60,60))
        self.hit_img = pygame.transform.scale(
            pygame.image.load("assets/images/hit.png").convert_alpha(), (60,60))

        self.player_speed = 7
        self.lives = 3
        self.reset_player()

        self.hit_timer = 0
        self.flash_toggle = False

        self.bullets = []
        self.enemy_bullets = []

        self.wave = 1
        self.wave_timer = 120
        self.enemy_shoot_timer = 0

        self.alien1 = pygame.transform.scale(
            pygame.image.load("assets/images/alien1.png").convert_alpha(), (50,50))
        self.alien2 = pygame.transform.scale(
            pygame.image.load("assets/images/alien2.png").convert_alpha(), (60,60))

        self.shoot_sfx = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.hit_sfx = pygame.mixer.Sound("assets/sounds/hit.wav")

        self.font = pygame.font.SysFont("arial", 28)
        self.big_font = pygame.font.SysFont("arial", 80, bold=True)
        self.wave_font = pygame.font.SysFont("arial", 70, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 40, bold=True)

        self.pause_options = ["RESUME", "MAIN MENU"]
        self.pause_selected = 0

        self.score = 0
        self.highscore = self.load_highscore()

        self.enemies = []
        self.create_wave()

    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            return int(open(HIGHSCORE_FILE).read())
        return 0

    def save_highscore(self):
        if self.score > self.highscore:
            open(HIGHSCORE_FILE, "w").write(str(self.score))

    def reset_player(self):
        self.player_rect = self.player_img.get_rect(center=(self.WIDTH//2, self.HEIGHT-80))

    def create_wave(self):
        self.enemies.clear()
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.reset_player()
        self.wave_timer = 120
        self.state = self.WAVE_DELAY

        cols = 10
        spacing = self.WIDTH // (cols + 1)
        rows = min(self.wave + 1, 5)

        for r in range(rows):
            for c in range(cols):
                strong = random.random() < 0.25
                img = self.alien2 if strong else self.alien1
                hp = 2 if strong else 1
                rect = img.get_rect(center=((c+1)*spacing, 100 + r*80))
                self.enemies.append({"rect": rect, "img": img, "hp": hp})

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == self.PLAYING:
                        self.state = self.PAUSED
                    elif self.state == self.PAUSED:
                        self.state = self.PLAYING

                if self.state == self.PAUSED:
                    if event.key == pygame.K_UP:
                        self.pause_selected = (self.pause_selected - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        self.pause_selected = (self.pause_selected + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.pause_selected == 0:
                            self.state = self.PLAYING
                        else:
                            self.save_highscore()
                            return "menu"

                if self.state == self.GAMEOVER and event.key == pygame.K_RETURN:
                    self.save_highscore()
                    return "menu"

                if self.state == self.PLAYING and event.key == pygame.K_SPACE:
                    self.bullets.append(
                        pygame.Rect(self.player_rect.centerx-2,
                                    self.player_rect.top, 4, 10))
                    self.shoot_sfx.play()
        return None

    def update(self):
        if self.state == self.WAVE_DELAY:
            self.wave_timer -= 1
            if self.wave_timer <= 0:
                self.state = self.PLAYING
            return

        if self.state != self.PLAYING:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.player_speed

        self.player_rect.x = max(0, min(self.player_rect.x,
                                        self.WIDTH - self.player_rect.width))

        if self.hit_timer > 0:
            self.hit_timer -= 1
            self.flash_toggle = not self.flash_toggle

        for b in self.bullets[:]:
            b.y -= 10
            if b.bottom < 0:
                self.bullets.remove(b)

        self.enemy_shoot_timer += 1
        if self.enemy_shoot_timer > 60 and self.enemies:
            shooter = random.choice(self.enemies)
            self.enemy_bullets.append(
                pygame.Rect(shooter["rect"].centerx,
                            shooter["rect"].bottom, 6, 12))
            self.enemy_shoot_timer = 0

        for b in self.enemy_bullets[:]:
            b.y += 6
            if b.colliderect(self.player_rect):
                self.enemy_bullets.remove(b)
                self.lives -= 1
                self.hit_timer = 120
                self.hit_sfx.play()
                if self.lives <= 0:
                    self.lives = 0
                    self.state = self.GAMEOVER

        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if b.colliderect(e["rect"]):
                    e["hp"] -= 1
                    self.bullets.remove(b)
                    if e["hp"] <= 0:
                        self.enemies.remove(e)
                        self.score += 100
                    break

        if not self.enemies:
            self.wave += 1
            self.create_wave()

    def draw(self):
        self.screen.fill((0,0,0))

        if self.hit_timer > 0 and self.flash_toggle:
            self.screen.blit(self.hit_img, self.player_rect)
        else:
            self.screen.blit(self.player_img, self.player_rect)

        for b in self.bullets:
            pygame.draw.rect(self.screen, (0,255,255), b)
        for b in self.enemy_bullets:
            pygame.draw.rect(self.screen, (255,60,60), b)
        for e in self.enemies:
            self.screen.blit(e["img"], e["rect"])

        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255,255,255)), (20,20))
        self.screen.blit(self.font.render(f"Highscore: {self.highscore}", True, (180,180,180)), (20,50))
        self.screen.blit(self.font.render(f"Lives: {self.lives}", True, (255,80,80)), (20,80))

        if self.state == self.WAVE_DELAY:
            txt = self.wave_font.render(f"WAVE {self.wave}", True, (0,255,255))
            self.screen.blit(txt, txt.get_rect(center=(self.WIDTH//2, self.HEIGHT//2)))

        if self.state == self.PAUSED:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,160))
            self.screen.blit(overlay, (0,0))
            for i, opt in enumerate(self.pause_options):
                col = (255,255,255) if i == self.pause_selected else (120,120,120)
                txt = self.menu_font.render(opt, True, col)
                self.screen.blit(txt, txt.get_rect(center=(self.WIDTH//2, 300 + i*80)))

        if self.state == self.GAMEOVER:
            t = self.big_font.render("GAME OVER", True, (255,0,0))
            self.screen.blit(t, t.get_rect(center=(self.WIDTH//2, self.HEIGHT//2-40)))
            hint = self.font.render("Press ENTER to return to menu", True, (200,200,200))
            self.screen.blit(hint, hint.get_rect(center=(self.WIDTH//2, self.HEIGHT//2+40)))
