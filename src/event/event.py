import pygame
from src import global_vars as gv
from src.event import key_input
import time

def on_event(events):
    for event in events:
        match(event.type):            
            case pygame.QUIT:
                gv.running = False

def listen_keys():
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            gv.player.move("forward")
        if keys[pygame.K_a]:
            gv.player.move("left")
        if keys[pygame.K_s]:
            gv.player.move("back")
        if keys[pygame.K_d]:
            gv.player.move("right")
        time.sleep(0.01)
