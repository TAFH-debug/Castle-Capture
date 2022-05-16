import pygame


class Button:
    text: str
    counter: int

    def __init__(self, onclick, height=100, width=100,
                 sprite_path="./sprites/ohno.png",
                 x=0, y=0, text="Button",
                 font_size=50):
        self.font_size = font_size
        self.sprite = pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (width, height))
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.onclick = onclick
        self.width = width
        self.height = height
        self.font = None
        self.counter = 0

    def draw(self, display: pygame.Surface, dx, dy):
        if not self.font:
            self.font = pygame.font.Font(None, self.font_size)
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        x = self.rect.x + self.width // 2 - text_rect.width // 2
        y = self.rect.y + self.height // 2 - text_rect.height // 2
        display.blit(self.sprite, self.rect)
        display.blit(text, (x, y))

    def update(self):
        x = self.rect.x
        y = self.rect.y
        mx, my = pygame.mouse.get_pos()
        if x < mx < x + self.width and y < my < y + self.height:
            if pygame.mouse.get_pressed()[0]:
                self.counter += 1
                self.onclick(self)
                return True
        return False
