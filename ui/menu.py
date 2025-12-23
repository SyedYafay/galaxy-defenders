import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.options = ["START GAME", "OPTIONS", "CREDITS", "QUIT"]
        self.selected = 0

        self.title_font = pygame.font.SysFont("arial", 80, bold=True)
        self.option_font = pygame.font.SysFont("arial", 45)

        self.normal_color = (255, 255, 255)
        self.highlight_color = (0, 255, 255)

    def draw(self):
        title = self.title_font.render("GALAGA RETRO", True, (255, 255, 0))
        self.screen.blit(
            title,
            (self.width // 2 - title.get_width() // 2, int(self.height * 0.15))
        )

        start_y = int(self.height * 0.35)
        spacing = 70

        for i, option in enumerate(self.options):
            color = self.highlight_color if i == self.selected else self.normal_color
            text = self.option_font.render(option, True, color)
            x = self.width // 2 - text.get_width() // 2
            y = start_y + i * spacing
            self.screen.blit(text, (x, y))

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.options)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.options)
