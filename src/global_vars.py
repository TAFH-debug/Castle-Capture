import pygame
from src.entity import unitc
from src.entity.player import Player
from src.ui.camera import Camera
from src.enviroment.world import World

def init():
    global running
    global camera
    global player
    global units
    global world
    world = World()
    units = list[unitc.Unit]()
    player = Player()
    running = True
    camera = Camera()
    

