import pygame, random, os, math

HIGHSCORE_FILE = "highscore.txt"

class Spark:
    def __init__(self, pos):
        self.x, self.y = pos
        angle = random.uniform(0, math.pi*2)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle)*speed
        self.vy = math.sin(angle)*speed
        self.life = 30
        self.radius = random.randint(2,4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life/30))
            surf = pygame.Surface((self.radius*2,)*2, pygame.SRCALPHA)
            pygame.draw.circle(surf, (255,200,50,alpha),
                               (self.radius,self.radius), self.radius)
            screen.blit(surf, (self.x, self.y))

class GameScene:
    def __init__(self, screen, sfx_volume):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        self.PLAYING, self.PAUSED, self.GAMEOVER, self.WAVE_DELAY = \
            "playing","paused","gameover","wave_delay"
        self.state = self.WAVE_DELAY

        self.player_img = pygame.transform.scale(
            pygame.image.load("assets/images/ship1.png").convert_alpha(), (60,60))
        self.hit_img = pygame.transform.scale(
            pygame.image.load("assets/images/hit.png").convert_alpha(), (60,60))

        self.player_speed = 7
        self.lives = 3
        self.reset_player()

        self.hit_timer = 0
        self.flash_timer = 0
        self.show_hit_sprite = False
        self.sparks = []

        self.bullets, self.enemy_bullets = [], []

        self.wave, self.wave_timer = 1, 120
        self.enemy_shoot_timer = 0

        self.alien1 = pygame.transform.scale(
            pygame.image.load("assets/images/alien1.png").convert_alpha(), (50,50))
        self.alien2 = pygame.transform.scale(
            pygame.image.load("assets/images/alien2.png").convert_alpha(), (60,60))

        self.shoot_sfx = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.hit_sfx = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.set_sfx_volume(sfx_volume)

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

    def set_sfx_volume(self, v):
        self.shoot_sfx.set_volume(v)
        self.hit_sfx.set_volume(v)

    def load_highscore(self):
        return int(open(HIGHSCORE_FILE).read()) if os.path.exists(HIGHSCORE_FILE) else 0

    def save_highscore(self):
        if self.score > self.highscore:
            open(HIGHSCORE_FILE,"w").write(str(self.score))

    def reset_player(self):
        self.player_rect = self.player_img.get_rect(
            center=(self.WIDTH//2, self.HEIGHT-80))

    def create_wave(self):
        self.enemies.clear()
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.reset_player()
        self.wave_timer = 120
        self.state = self.WAVE_DELAY

        cols = 10
        spacing = self.WIDTH//(cols+1)
        rows = min(self.wave+1,5)

        for r in range(rows):
            for c in range(cols):
                strong = random.random()<0.25
                img = self.alien2 if strong else self.alien1
                hp = 2 if strong else 1
                rect = img.get_rect(center=((c+1)*spacing,100+r*80))
                self.enemies.append({"rect":rect,"img":img,"hp":hp})

    def handle_input(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.state = self.PAUSED if self.state==self.PLAYING else self.PLAYING
                if self.state==self.PAUSED:
                    if e.key==pygame.K_UP:
                        self.pause_selected=(self.pause_selected-1)%2
                    elif e.key==pygame.K_DOWN:
                        self.pause_selected=(self.pause_selected+1)%2
                    elif e.key==pygame.K_RETURN:
                        if self.pause_selected==1:
                            self.save_highscore()
                            return "menu"
                        self.state=self.PLAYING
                if self.state==self.GAMEOVER and e.key==pygame.K_RETURN:
                    self.save_highscore()
                    return "menu"
                if self.state==self.PLAYING and e.key==pygame.K_SPACE:
                    self.bullets.append(
                        pygame.Rect(self.player_rect.centerx-2,
                                    self.player_rect.top,4,10))
                    self.shoot_sfx.play()
        return None

    def update(self):
        if self.state==self.WAVE_DELAY:
            self.wave_timer-=1
            if self.wave_timer<=0:
                self.state=self.PLAYING
            return
        if self.state!=self.PLAYING:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.player_rect.x-=self.player_speed
        if keys[pygame.K_RIGHT]: self.player_rect.x+=self.player_speed
        self.player_rect.x = max(0,min(self.player_rect.x,
                                       self.WIDTH-self.player_rect.width))

        # HIT EFFECT LOGIC
        if self.hit_timer>0:
            self.hit_timer-=1
            self.flash_timer+=1
            if self.flash_timer>=30:
                self.flash_timer=0
                self.show_hit_sprite=not self.show_hit_sprite
        else:
            self.show_hit_sprite=False

        for s in self.sparks[:]:
            s.update()
            if s.life<=0:
                self.sparks.remove(s)

        for b in self.bullets[:]:
            b.y-=10
            if b.bottom<0:
                self.bullets.remove(b)

        self.enemy_shoot_timer+=1
        if self.enemy_shoot_timer>60 and self.enemies:
            shooter=random.choice(self.enemies)
            self.enemy_bullets.append(
                pygame.Rect(shooter["rect"].centerx,
                            shooter["rect"].bottom,6,12))
            self.enemy_shoot_timer=0

        for b in self.enemy_bullets[:]:
            b.y+=6
            if b.colliderect(self.player_rect):
                self.enemy_bullets.remove(b)
                self.lives-=1
                self.hit_timer=120
                self.flash_timer=0
                self.show_hit_sprite=True  # IMMEDIATE
                self.hit_sfx.play()
                for _ in range(15):
                    self.sparks.append(Spark(self.player_rect.center))
                if self.lives<=0:
                    self.lives=0
                    self.state=self.GAMEOVER

        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if b.colliderect(e["rect"]):
                    e["hp"]-=1
                    self.bullets.remove(b)
                    if e["hp"]<=0:
                        self.enemies.remove(e)
                        self.score+=100
                    break

        if not self.enemies:
            self.wave+=1
            self.create_wave()

    def draw(self):
        self.screen.fill((0,0,0))
        sprite = self.hit_img if self.show_hit_sprite else self.player_img
        self.screen.blit(sprite,self.player_rect)

        for s in self.sparks:
            s.draw(self.screen)

        for b in self.bullets:
            pygame.draw.rect(self.screen,(0,255,255),b)
        for b in self.enemy_bullets:
            pygame.draw.rect(self.screen,(255,60,60),b)
        for e in self.enemies:
            self.screen.blit(e["img"],e["rect"])

        self.screen.blit(self.font.render(f"Score: {self.score}",True,(255,255,255)),(20,20))
        self.screen.blit(self.font.render(f"Highscore: {self.highscore}",True,(180,180,180)),(20,50))
        self.screen.blit(self.font.render(f"Lives: {self.lives}",True,(255,80,80)),(20,80))

        if self.state==self.WAVE_DELAY:
            t=self.wave_font.render(f"WAVE {self.wave}",True,(0,255,255))
            self.screen.blit(t,t.get_rect(center=(self.WIDTH//2,self.HEIGHT//2)))

        if self.state==self.PAUSED:
            overlay=pygame.Surface((self.WIDTH,self.HEIGHT),pygame.SRCALPHA)
            overlay.fill((0,0,0,160))
            self.screen.blit(overlay,(0,0))
            for i,opt in enumerate(self.pause_options):
                col=(255,255,255) if i==self.pause_selected else (120,120,120)
                txt=self.menu_font.render(opt,True,col)
                self.screen.blit(txt,txt.get_rect(center=(self.WIDTH//2,300+i*80)))

        if self.state==self.GAMEOVER:
            t=self.big_font.render("GAME OVER",True,(255,0,0))
            self.screen.blit(t,t.get_rect(center=(self.WIDTH//2,self.HEIGHT//2-40)))
            h=self.font.render("Press ENTER to return to menu",True,(200,200,200))
            self.screen.blit(h,h.get_rect(center=(self.WIDTH//2,self.HEIGHT//2+40)))
