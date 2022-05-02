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

can_move_up = True
can_move_down = True
can_move_left = True
can_move_right = True

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
    global can_move_up
    global can_move_down
    global can_move_left
    global can_move_right

    coords = (player.unit.x // TILESIZE, player.unit.y // TILESIZE)
    up = base.tryf(tiles.get, (coords[0] + 1, coords[1]))
    down = base.tryf(tiles.get, (coords[0] - 1, coords[1]))
    left = base.tryf(tiles.get, (coords[0], coords[1] - 1))
    right = base.tryf(tiles.get, (coords[0], coords[1] + 1))

    if up and not up.is_water and pygame.sprite.collide_rect(up, player.unit):
        can_move_up = False
    else:
        can_move_up = True

    if down and not down.is_water and pygame.sprite.collide_rect(down, player.unit):
        can_move_down = False
    else:
        can_move_down = True

    if right and not right.is_water and pygame.sprite.collide_rect(right, player.unit):
        can_move_right = False
    else:
        can_move_right = True

    if left and not left.is_water and pygame.sprite.collide_rect(left, player.unit):
        can_move_left = False
    else:
        can_move_left = True


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
            if not can_move_up:
                return
            if self.unit.rot_angle < 180:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            elif self.unit.rot_angle > 180:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            self.unit.y += 1
            cam_y += 1
        case "back":
            if not can_move_down:
                return
            if self.unit.rot_angle >= 180:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            elif self.unit.rot_angle < 180 and self.unit.rot_angle != 0:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            self.unit.y -= 1
            cam_y -= 1
        case "right":
            if not can_move_right:
                return
            if 90 < self.unit.rot_angle < 270:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            elif self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            self.unit.x += 1
            cam_x += 1
        case "left":
            if not can_move_left:
                return
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
