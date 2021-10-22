import re
import pygame
import os
from fractions import Fraction
from random import randint

# Colors
paint = {
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "red": (255, 0, 0)
}

# Window
screen_size = (1280, 720)

aspect_ratio = str(Fraction(screen_size[0], screen_size[1])).split("/")
grid_scale = 1

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake eats apples??")

class Grid(object):

    def __init__(self):

        tile_size = screen_size[0]/int(aspect_ratio[0])
        tile_size //= grid_scale
        max_width = screen_size[0]//tile_size
        max_height = screen_size[1]//tile_size

        self.tile_size = tile_size
        self.max_width = max_width
        self.max_height = max_height

    def get_loc(self, x, y):
        
        w_pixel = x * self.tile_size
        h_pixel = y * self.tile_size
        result = (w_pixel, h_pixel)

        return result

    def random_loc(self):
        
        result = (randint(0, self.max_width), randint(self.max_height))
        return result

    def move(self):
        pass

    def random_loc_border(self):
        pass

def play():
    carry_on = True

    clock = pygame.time.Clock()

    while carry_on:

        carry_on = event_handler()
        
        screen_render()
        pygame.display.update()

        clock.tick(60)

    pygame.quit()

def event_handler():

    result = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            result = False
    
    return result

def screen_render():
    
    screen.fill(paint["black"])

    screen.blit(grid_marker, (0, 0))

def image_loader(name, scale):

    result = pygame.image.load(os.path.join("Assets", f"{name}"))

    if scale != "default":
        result = pygame.transform.scale(result, scale)
    
    result = result.convert()

    return result

# loading assets
grid_marker = image_loader("test_grid_loc_marker.png", (80, 80))

play()