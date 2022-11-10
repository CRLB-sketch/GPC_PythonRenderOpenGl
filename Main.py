import pygame
from pygame.locals import *

from Shaders import *
from GlOpen import *
from ModelOGL import Model

from math import cos, sin, radians

width = 960
height = 540

delta_time = 0 # Diferencia entre cuadros

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock() # Esto servirá para tomar el control de los FPS

rend = Renderer(screen)

rend.set_shaders(vertex_shader, fragment_shader)

rend.target.z = -5

face = Model("models/model.obj", "models/model.bmp")

face.position.z -= 5
face.scale.x = 2
face.scale.y = 2
face.scale.z = 2

rend.scene.append(face)

is_running = True

while is_running:

    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
                
            elif event.key == pygame.K_z:
                rend.filled_mode()
            elif event.key == pygame.K_x:
                rend.wireframe_mode()
            
    # !++++++++++++++++++++++++++++++++
    if keys[K_q]:
        if rend.cam_distance > 2:
            rend.cam_distance -= 2 * delta_time
    elif keys[K_e]:
        if rend.cam_distance < 10:
            rend.cam_distance += 2 * delta_time
    # !++++++++++++++++++++++++++++++++
            
    if keys[K_a]:
        rend.angle -= 30 * delta_time
    elif keys[K_d]:
        rend.angle += 30 * delta_time
    
    if keys[K_w]:
        if rend.cam_position.y < 2:
            rend.cam_position.y += 5 * delta_time
    elif keys[K_s]:
        if rend.cam_position.y > -2:
            rend.cam_position.y -= 5 * delta_time
    # !++++++++++++++++++++++++++++++++
    
    rend.target.y = rend.cam_position.y
    
    rend.cam_position.x = rend.target.x + sin(radians(rend.angle)) * rend.cam_distance
    rend.cam_position.z = rend.target.z + cos(radians(rend.angle)) * rend.cam_distance
    
    if keys[K_LEFT]:
        rend.point_light.x -= 10 * delta_time
    elif keys[K_RIGHT]:
        rend.point_light.x += 10 * delta_time
    elif keys[K_UP]:
        rend.point_light.y += 10 * delta_time
    elif keys[K_DOWN]:
        rend.point_light.y -= 10 * delta_time
    
    # !------------------------------------------------------------------------------------
    # ! --- MANEJADOR DE SHADERS ----------------------------------------------------------
    if keys[K_1]:
        rend.set_shaders(vertex_shader, fragment_shader)
    elif keys[K_2]:
        rend.set_shaders(vertex_shader_color, fragment_shader_color)
    # !------------------------------------------------------------------------------------
        
    delta_time = clock.tick(60) / 1000
    rend.time += delta_time
    
    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
