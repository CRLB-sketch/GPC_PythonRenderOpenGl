import pygame
from pygame.locals import *

from Shaders import *
from GlOpen import *
from ModelOGL import Model
# import ModelOGL

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock() # Esto servirá para tomar el control de los FPS

delta_time = 0 # Diferencia entre cuadros

rend = Renderer(screen)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
rend.set_shaders(vertex_shader, fragment_shader)

face = Model("models/model.obj")

face.position.z -= 10

rend.scene.append(face)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
# rend.set_shaders(vertex_shader, fragment_shader)

# triangle = [
#     -0.5, -0.5, 0,   1, 0, 0,
#         0, 0.5, 0,   0, 1, 0,
#      0.5, -0.5, 0,    0, 0, 1
# ]

# rend.scene.append(Buffer(triangle))
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++

is_running = True

while is_running:

    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    
    if keys[K_LEFT]:
        rend.cam_position.x -= 10 * delta_time
        
    elif keys[K_RIGHT]:
        rend.cam_position.x += 10 * delta_time
        
    delta_time = clock.tick(60) / 1000
    
    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
