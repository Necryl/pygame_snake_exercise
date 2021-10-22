import pygame

# Colors
paint = {
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "red": (255, 0, 0)
}

# Window
screen_size = (900, 700)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake eats apples??")

def play():
    carry_on = True

    clock = pygame.time.Clock()

    while carry_on:

        carry_on = handle_events()

        screen.fill(paint["black"])

        pygame.display.update()

    pygame.quit()


def handle_events():

    result = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            result = False
    
    return result

play()