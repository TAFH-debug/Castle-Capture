import math
import time
import threading
from abc import abstractmethod

from ..base import GameObject, zero
import pygame

TILESIZE = 60


class UnitType:
    sprite_file: str
    speed: int
    destroyed_sprite: str
    prt_destr_sprite: str

    def __init__(self, sprite_file: str, speed: int, destroyed_sprite: str = None, prt_destr_sprite: str = None):
        if not destroyed_sprite:
            self.destroyed_sprite = sprite_file
        else:
            self.destroyed_sprite = destroyed_sprite
        if not prt_destr_sprite:
            self.prt_destr_sprite = sprite_file
        else:
            self.prt_destr_sprite = prt_destr_sprite
        self.speed = speed
        self.sprite_file = sprite_file


class Bullet(GameObject):
    tx: int
    ty: int
    lifetime: int
    destroyed: bool
    destroying: bool
    damage: int

    def __init__(self, x: int, y: int, targetx: int, targety: int, owner, speed=3, lifetime=100, damage=20):
        super().__init__("./sprites/ship_parts/cannonBall.png", x, y)
        self.damage = damage
        self.owner = owner
        self.tx = targetx
        self.ty = targety
        self.lifetime = lifetime
        dx = targetx - x
        dy = targety - y
        rng = math.sqrt(dx**2 + dy**2)
        self.speed_x = (speed / rng) * dx
        self.speed_y = (speed / rng) * dy
        self.destroyed = False
        self.destroying = False

    def draw(self, display: pygame.Surface, dx, dy):
        super().draw(display, dx, dy)

    def destroy(self):
        exp1 = pygame.image.load("./sprites/effects/explosion2.png").convert_alpha()
        self.sprite = exp1
        time.sleep(1)
        self.destroyed = True

    def update(self):
        if self.destroying:
            return
        if self.lifetime == 0:
            self.destroying = True
            threading.Thread(target=self.destroy, daemon=True).start()
            return
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1


class Healthc(GameObject):
    health: int
    max_health: int
    to_remove: bool

    def __init__(self, sprite="./sprites/ohno.png", x=0, y=0, health=100):
        super().__init__(sprite, x, y)
        self.health = self.max_health = health
        self.to_remove = False

    def remove_after(self, sec: int):
        time.sleep(sec)
        self.to_remove = True

    @abstractmethod
    def destroy(self):
        pass


class Unit(Healthc):
    type: UnitType
    bullets: list
    timeout: int
    team: str

    def __init__(self, _type: UnitType, x: int, y: int, health=100, team="player"):
        super().__init__(_type.sprite_file, x, y)
        self.max_timeout = 100
        self.timeout = 0
        self.type = _type
        self.bullets = []
        self.team = team
        self.destroyed = False

    def is_owner(self, bullet):
        return bullet.owner.team == self.team

    def destroy(self):
        self.sprite = pygame.image.load(self.type.destroyed_sprite).convert_alpha()
        self.shoot = zero
        self.update = zero
        self.destroyed = True
        threading.Thread(target=self.remove_after, args=(4,), daemon=True).start()

    def draw(self, display: pygame.Surface, dx, dy):
        super().draw(display, dx, dy)
        pygame.draw.rect(display, (255, 0, 0), (self.rect.x, self.rect.y - 20, 100, 20))
        pygame.draw.rect(display, (0, 255, 0), (self.rect.x, self.rect.y - 20, 100 * self.health / self.max_health, 20))
        for i in self.bullets:
            i.draw(display, dx, dy)

    def update(self):
        if self.health / self.max_health < 0.5:
            self.sprite = pygame.image.load(self.type.prt_destr_sprite).convert_alpha()
        idx = None
        for i in range(len(self.bullets)):
            bullet = self.bullets[i]
            if bullet.destroyed:
                idx = i
            bullet.update()
        if idx != None:
            self.bullets.pop(idx)
        self.timeout -= 1

    def shoot(self, sx, sy, bullet=None):
        if self.timeout > 0:
            return
        width = self.sprite.get_width() // 2
        if not bullet:
            bullet = Bullet(self.x + width, self.y - width, sx, sy, self)
        self.bullets.append(bullet)
        self.timeout = self.max_timeout


class CastleTile(Unit):

    def __init__(self, sprite, spritedst, spriteprtdst, x=0, y=0, health=300):
        super().__init__(UnitType(sprite, 0, spritedst, spriteprtdst), x, y, health)
        self.max_timeout = 400

    def ai(self, targetx, targety):
        if math.sqrt((self.x - targetx) ** 2 + (self.y - targety) ** 2) > 600:
            if self.timeout == 0:
                return
            self.timeout -= 1
            return
        width = self.sprite.get_width() // 2
        bullet = Bullet(self.x + width, self.y - width, targetx, targety, self, 2, 300, 10)
        self.shoot(targetx, targety, bullet)


class Castle:

    tiles: list

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        pref = "sprites/tiles/tile_"
        self.tiles = [
            CastleTile(pref + "77.png", None, None, x, y),
            CastleTile(pref + "16.png", pref + "90.png", pref + "92.png", x + TILESIZE, y),
            CastleTile(pref + "32.png", pref + "89.png", pref + "91.png", x, y - TILESIZE),
            CastleTile(pref + "78.png", None, None, x + 2 * TILESIZE, y),
            CastleTile(pref + "93.png", None, None, x, y - 2 * TILESIZE),
            CastleTile(pref + "32.png", pref + "89.png", pref + "91.png", x + 2 * TILESIZE, y - TILESIZE),
            CastleTile(pref + "16.png", pref + "90.png", pref + "92.png", x + TILESIZE, y - 2 * TILESIZE),
            CastleTile(pref + "94.png", None, None, x + 2 * TILESIZE, y - 2 * TILESIZE),
        ]

    def ai(self, targetx, targety):
        for i in self.tiles: i.ai(targetx, targety)


class Player:
    unit: Unit

    def __init__(self, unit=None):
        self.unit = unit
