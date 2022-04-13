import pygame
from src import global_vars
from src.event import key_input
import time

def on_event(events):
    for event in events:
        match(event.type):            
            case pygame.QUIT:
                global_vars.running = False

def listen_keys():
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            global_vars.player.unit.go_forward()
        if keys[pygame.K_a]:
            key_input.a_key()
        if keys[pygame.K_s]:
            key_input.s_key()
        if keys[pygame.K_d]:
            key_input.d_key()
        time.sleep(0.01)
