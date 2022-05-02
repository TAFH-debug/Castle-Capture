import pygame
from pygame.sprite import AbstractGroup


class GameObject(pygame.sprite.Sprite):
    sprite: pygame.Surface
    sprite_updated: pygame.Surface
    rect: pygame.Rect
    x: int
    y: int
    rot_angle: int

    def __init__(self, sprite="sprites/ohno.png", x=0, y=0, *groups: AbstractGroup):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.rot_angle = 0
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite_updated = self.sprite.copy()
        self.rect = self.sprite.get_rect()

    def draw(self, display: pygame.Surface, dx, dy):
        self.sprite_updated = pygame.transform.rotate(self.sprite, self.rot_angle)
        old_center = self.rect.center
        self.rect = self.sprite_updated.get_rect()
        self.rect.center = old_center
        self.rect.x = -(display.get_width() / 2) + (self.x - dx)
        self.rect.y = (display.get_height() / 2) - (self.y - dy)
        display.blit(self.sprite_updated, self.rect)

    def update(self):
        pass


class Camera:
    lock_obj: GameObject
    x: int
    y: int

    def __init__(self, lock_object=None):
        self.lock_obj = lock_object
        self.x = 0
        self.y = 0
