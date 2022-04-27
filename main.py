import pygame
import threading
from src.core import event
from src.core.entity import *
import time

display = pygame.display.set_mode((1200, 700))
drawable = []
running = True
player = Player()
x = 0
y = 0


def init():
    pygame.init()
    klisten_thread = threading.Thread(target=listen_keys)
    klisten_thread.daemon = True
    klisten_thread.start()


def draw():
    display.fill((0, 0, 0))
    for i in drawable:
        i.draw(display, x, y)
    pygame.display.flip()


def debug_info():
    print(drawable[0].x)
    print(drawable[0].y)
    time.sleep(0.2)


def main():
    player.unit = Unit(UnitType("sprites/ships/ship (1).png", 1), 1000, 100)
    enemy = GameObject("sprites/ships/ship (4).png", 1000, 100)
    drawable.append(player.unit)
    #drawable.append(enemy)
    while event.is_quit(pygame.event.get()):
        draw()


def listen_keys():
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            debug_info()
        if keys[pygame.K_w]:
            player.move("forward")
        if keys[pygame.K_a]:
            player.move("left")
        if keys[pygame.K_s]:
            player.move("back")
        if keys[pygame.K_d]:
            player.move("right")
        time.sleep(0.01)


if __name__ == "__main__":
    init()
    main()
