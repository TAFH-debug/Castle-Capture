import threading
import time

import pygame.sprite

from src.core import *

world_size = 20
display = pygame.display.set_mode((1200, 700))
drawable = []
running = True
player = Player()
cam_x = 0
cam_y = 0
tiles = Tiles(world_size)
clock = pygame.time.Clock()

def init():
    pygame.init()
    klisten_thread = threading.Thread(target=listen_keys)
    klisten_thread.daemon = True
    klisten_thread.start()


def draw_fps():
    f1 = pygame.font.Font(None, 20)
    text = f1.render(str(int(clock.get_fps())), True, (0, 0, 0))
    display.blit(text, (0, 0))


def draw():
    display.fill((0, 0, 0))
    tiles.draw(display, cam_x, cam_y)
    for i in drawable:
        i.draw(display, cam_x, cam_y)
    draw_fps()
    pygame.display.flip()


def debug_info():
    print(drawable[0].x)
    print(drawable[0].y)
    time.sleep(0.2)


def physics():
    global cam_y
    global cam_x
    pl_coords = (player.unit.x + 30, player.unit.y + 30)
    pl_coords2 = (player.unit.x, player.unit.y)
    coords = ((player.unit.x + 30) // TILESIZE, (player.unit.y + 30) // TILESIZE)
    nearby = tiles.get_nearby_tiles(coords)
    for i in nearby:
        if i.is_water: continue
        if gen.in_range(pl_coords, (i.x, i.y), TILESIZE) or gen.in_range(pl_coords2, (i.x, i.y), TILESIZE):
            if player.unit.x - i.x > player.unit.y - i.y:
                dx = player.unit.x - i.x
                player.unit.x -= dx
                cam_x -= dx
            else:
                dy = player.unit.y - i.y
                player.unit.y -= dy
                cam_y -= dy


def main():
    global tiles
    player.unit = Unit(UnitType("sprites/ships/ship (1).png", 1), 1000, 100)
    enemy = GameObject("sprites/ships/ship (4).png", 1000, 100)
    drawable.append(player.unit)
    drawable.append(enemy)
    tiles = gen.generate_map(world_size)
    while is_quit(pygame.event.get()):
        physics()
        clock.tick(60)
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
