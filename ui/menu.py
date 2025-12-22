import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.font = pygame.font.SysFont("arial", 45)
        self.options = ["Play", "Options", "Credits", "Exit"]
        self.selected = 0

        self.text_color = (255, 255, 255)
        self.highlight_color = (0, 255, 255)

    def draw(self):
        self.screen.fill((0, 0, 50))

        title_font = pygame.font.SysFont("arial", 80, bold=True)
        title = title_font.render("GALAGA RETRO", True, (255, 255, 0))
        self.screen.blit(
            title,
            (self.width // 2 - title.get_width() // 2, int(self.height * 0.15))
        )

        start_y = int(self.height * 0.35)
        spacing = 70

        for i, option in enumerate(self.options):
            color = self.highlight_color if i == self.selected else self.text_color
            text = self.font.render(option, True, color)
            self.screen.blit(
                text,
                (self.width // 2 - text.get_width() // 2, start_y + i * spacing)
            )

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.options)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.options)

    def select(self):
        return self.options[self.selected]
