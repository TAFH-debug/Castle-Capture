import pygame


def is_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True
