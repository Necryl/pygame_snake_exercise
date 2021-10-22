import pygame
import os
from fractions import Fraction
from random import randint

# Colors
paint = {
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255)
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
        # subtracting 1 to convert it into cardinal values
        max_width -= 1
        max_height -= 1

        self.tile_size = tile_size
        self.max_width = max_width
        self.max_height = max_height

    def pixelize(self, loc):
        
        x = loc[0] * self.tile_size
        y = loc[1] * self.tile_size
        result = (x, y)

        return result

    def random_loc(self, mode="normal"):
        
        if mode == "normal":
            result = (randint(0, self.max_width), randint(0, self.max_height))
        elif mode == "border":
            dice = randint(0, 3) # [0 == top], [1 == bottom], [2 == left], [3 == right]
            x = randint(0, self.max_width)
            y = randint(0, self.max_height)
            if dice == 0:
                y = 0
            elif dice == 1:
                y = self.max_height
            elif dice == 2:
                x = 0
            elif dice == 3:
                x = self.max_width
            result = (x, y)
        else:
            raise Exception(f"ERROR: random_loc() function didn't expect argument -> '{mode}'")


        return result

    def move(self, current_loc, direction, at_border='tp'):
        
        x = current_loc[0]
        y = current_loc[1]
        border = False

        if direction == 'up':
            if y == 0:
                y = self.max_height
                border = True
            else:
                y -= 1
        elif direction == 'down':
            if y == self.max_height:
                y = 0
                border = True
            else:
                y += 1
        elif direction == 'left':
            if x == 0:
                x = self.max_width
                border = True
            else:
                x -= 1
        elif direction == 'right':
            if x == self.max_width:
                x = 0
                border = True
            else:
                x += 1
        
        result = (x, y)

        if at_border != 'tp' and border == True:
            if direction == 'up' or direction == 'down':
                if at_border == 'new_line_f':
                    result = self.move(result, 'right')
                elif at_border == 'new_line_b':
                    result = self.move(result, 'left')
            elif direction == 'left' or direction == 'right':
                if at_border == 'new_line_f':
                    result = self.move(result, 'down')
                elif at_border == 'new_line_b':
                    result = self.move(result, 'up')

        return result

class Tile(object):

    def __init__(self):
        present_loc = None
        visual = (paint["blue"], 'color')
        bounds = None

        self.present_loc = present_loc
        self.visual = visual
        self.bounds = bounds
    
    def update_bounds(self, new_loc=None):
        if new_loc != None:
            self.present_loc = new_loc

        if self.present_loc != None:
            self.bounds = pygame.Rect(game_grid.pixelize(self.present_loc), (game_grid.tile_size, game_grid.tile_size))
        else:
            raise Exception("ERROR: self.present_loc is 'None'")

    def spawn(self, new_loc=None):
        
        if new_loc != None:
            self.update_bounds(new_loc)
        
        spawn_point = game_grid.pixelize(self.present_loc)

        if self.visual[1] == 'image':
            screen.blit(self.visual[0], spawn_point)
        elif self.visual[1] == 'color':
            pygame.draw.rect(screen, self.visual[0], self.bounds)
        else:
            raise Exception(f"ERROR: self.visual[1] contains invalid value '{self.visual[1]}'")

    def move(self, direction, at_border=None):

        self.present_loc = game_grid.move(self.present_loc, direction, at_border)
        self.update_bounds()

def play():
    carry_on = True

    clock = pygame.time.Clock()
    apple.update_bounds(game_grid.random_loc())
    screen.fill(paint["black"])

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

    apple.spawn()

def image_loader(name, scale):

    result = pygame.image.load(os.path.join("Assets", f"{name}"))

    if scale != "default":
        result = pygame.transform.scale(result, scale)
    
    result = result.convert()

    return result

# Creating grid
game_grid = Grid()

# Creating entities
box = Tile()
box.visual = (image_loader("test_grid_loc_marker.png", (game_grid.tile_size, game_grid.tile_size)), 'image')
box.present_loc = (0, 0)

cover = Tile()
cover.visual = (paint['black'], 'color')

apple = Tile()
apple.visual = (paint['red'], 'color')
apple.present_loc = (0, 0)
apple.update_bounds()



play()