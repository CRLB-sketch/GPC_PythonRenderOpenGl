import pygame
from pygame.locals import *

from Gl import Renderer

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock() # Esto servirá para tomar el control de los FPS

rend = Renderer(screen)

delta_time = 0 # Diferencia entre cuadros

is_running = True

while is_running:

    # keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    
    delta_time = clock.tick(60) / 1000
    
    rend.render()

    pygame.display.flip()

pygame.quit()
