import random
import threading
import time

from src.core import *

world_size = 10
display = pygame.display.set_mode((1200, 700))
drawable = []
running = True
player = Player()
cam_x = 0
cam_y = 0
tiles = Tiles(world_size)


def init():
    pygame.init()
    klisten_thread = threading.Thread(target=listen_keys)
    klisten_thread.daemon = True
    klisten_thread.start()


def get_random_tile_sprite():
    path = "sprites/tiles/tile_%n.png"
    n = random.randint(1, 96)
    if n < 10:
        n = "0" + str(n)
    else:
        n = str(n)
    return path.replace("%n", n)


def generate_map():
    for i in range(world_size):
        for j in range(world_size):
            tiles.set((i, j), Tile(get_random_tile_sprite()))


def draw():
    display.fill((0, 0, 0))
    for i in drawable:
        i.draw(display, cam_x, cam_y)
    tiles.draw(display, cam_x, cam_y)
    pygame.display.flip()


def debug_info():
    print(drawable[0].x)
    print(drawable[0].y)
    time.sleep(0.2)


def main():
    player.unit = Unit(UnitType("sprites/ships/ship (1).png", 1), 1000, 100)
    enemy = GameObject("sprites/ships/ship (4).png", 1000, 100)
    drawable.append(player.unit)
    drawable.append(enemy)
    generate_map()
    while is_quit(pygame.event.get()):
        draw()


def move(self, direction: str):
    global cam_x
    global cam_y
    match direction:
        case "forward":
            if self.unit.rot_angle < 180:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            elif self.unit.rot_angle > 180:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            self.unit.y += 1
            cam_y += 1
        case "back":
            if self.unit.rot_angle >= 180:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            elif self.unit.rot_angle < 180 and self.unit.rot_angle != 0:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            self.unit.y -= 1
            cam_y -= 1
        case "right":
            if 90 < self.unit.rot_angle < 270:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            elif self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            self.unit.x += 1
            cam_x += 1
        case "left":
            if self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            elif self.unit.rot_angle < 270:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            self.unit.x -= 1
            cam_x -= 1


def listen_keys():
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            debug_info()
        if keys[pygame.K_w]:
            move(player, "forward")
        if keys[pygame.K_a]:
            move(player, "left")
        if keys[pygame.K_s]:
            move(player, "back")
        if keys[pygame.K_d]:
            move(player, "right")
        time.sleep(0.01)


if __name__ == "__main__":
    init()
    main()
