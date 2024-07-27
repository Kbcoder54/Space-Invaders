import pygame,os


size = (800,600)
screen = pygame.display.set_mode(size)

running =  True
pygame.display.set_caption("Space Invaders")

color = 0, 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(color)
    pygame.display.update()