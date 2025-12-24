import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.options = ["START GAME", "OPTIONS", "CREDITS", "QUIT"]
        self.selected = 0

        self.title_font = pygame.font.SysFont("arial", 80, bold=True)
        self.option_font = pygame.font.SysFont("arial", 45)

        self.normal_color = (255,255,255)
        self.highlight_color = (0,255,255)

        self.start_y = int(self.height * 0.35)
        self.spacing = 70

    def draw(self):
        title = self.title_font.render("GALAXY DEFENDERS", True, (255,255,0))
        self.screen.blit(
            title,
            title.get_rect(center=(self.width//2, int(self.height*0.15)))
        )

        for i, option in enumerate(self.options):
            color = self.highlight_color if i == self.selected else self.normal_color
            text = self.option_font.render(option, True, color)
            self.screen.blit(
                text,
                text.get_rect(center=(self.width//2, self.start_y + i*self.spacing))
            )

    def get_selected_y(self):
        return self.start_y + self.selected * self.spacing - 10

    def move_up(self):
        self.selected = (self.selected - 1) % len(self.options)

    def move_down(self):
        self.selected = (self.selected + 1) % len(self.options)
