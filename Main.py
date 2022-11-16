import pygame
from pygame.locals import *

from Shaders import *
from GlOpen import *
from ModelOGL import Model

from math import cos, sin, radians

width = 960
height = 540
    
def createModel(direction : str, texture : str, texture_for_mixture : str, position = [0, 0], scales = [0, 0, 0]):
    model = Model(direction, texture, texture_for_mixture)
    model.position.y -= position[0]
    model.position.z -= position[1]
    model.scale.x = scales[0]
    model.scale.y = scales[1]
    model.scale.z = scales[2]
    return model

def all_keyboard_input(keys):
    # !------------------------------------------------------------------------------------
    # ! --- ZOOM OBJETO -------------------------------------------------------------------
    if keys[K_q]:
        if rend.cam_distance > 2:
            rend.cam_distance -= 2 * delta_time
    elif keys[K_e]:
        if rend.cam_distance < 10:
            rend.cam_distance += 2 * delta_time
    # !------------------------------------------------------------------------------------
    # ! --- MOVIMIENTO HORIZONTAL ---------------------------------------------------------
    if keys[K_a]:
        rend.angle_x -= 30 * delta_time
    elif keys[K_d]:
        rend.angle_x += 30 * delta_time
    # ! --- MOVIMIENTO VERTICAL -----------------------------------------------------------
    if keys[K_w]:
        rend.angle_y += 30 * delta_time
    elif keys[K_s]:
        rend.angle_y -= 30 * delta_time
    # !------------------------------------------------------------------------------------
    # ! --- ROTACION EN EJE X -------------------------------------------------------------
    rend.cam_position.x = rend.target.x + sin(radians(rend.angle_x)) * rend.cam_distance
    rend.cam_position.z = rend.target.z + cos(radians(rend.angle_x)) * rend.cam_distance
    # ! --- ROTACION EN EJE Y -------------------------------------------------------------
    rend.cam_position.y = rend.target.y + sin(radians(rend.angle_y)) * rend.cam_distance
    # !------------------------------------------------------------------------------------
    # ! --- MANEJADOR DE LUCES ------------------------------------------------------------
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
    if keys[K_2]:
        rend.set_shaders(vertex_shader_animation, fragment_shader_animation)
    if keys[K_3]:
        rend.set_shaders(vertex_shader_color, fragment_shader_color)
    if keys[K_4]:
        rend.set_shaders(vertex_shader_best, toon_shader_fs)
    if keys[K_5]:
        rend.set_shaders(vertex_shader_best, rainbow_fs)
    if keys[K_6]:
        rend.set_shaders(mix_two_textures_vs, mix_two_textures_fs)    
    if keys[K_7]:
        rend.set_shaders(party_extreme_vs, party_extreme_fs)
    # !------------------------------------------------------------------------------------
    # ! --- PARA CAMBIAR DE MODELOS -------------------------------------------------------
    if keys[K_f]: # Cara humana
        model_actual = model_1
        rend.scene[0] = model_actual
    if keys[K_g]: # Pinguino de madagascar
        model_actual = model_2
        rend.scene[0] = model_actual
    if keys[K_h]: # Un Mishi
        model_actual = model_3
        rend.scene[0] = model_actual
    if keys[K_j]: # Joker has a Gun
        model_actual = model_4
        rend.scene[0] = model_actual
    if keys[K_k]: # Iguana
        model_actual = model_5
        rend.scene[0] = model_actual
    # !------------------------------------------------------------------------------------

if __name__ == "__main__":

    delta_time = 0 # Diferencia entre cuadros

    pygame.init()

    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock() # Esto servirá para tomar el control de los FPS
    
    rend = Renderer(screen)

    rend.set_shaders(vertex_shader, fragment_shader)

    rend.target.z = -5

    model_actual = None
    model_1 = createModel("resources/models/Cat.obj", "resources/textures/Cat.bmp", "resources/textures/earthDay.bmp", [1, 5], [0.07, 0.07, 0.07])
    model_2 = createModel("resources/models/PenguinBaseMesh.obj", "resources/textures/Penguin.bmp", "resources/textures/earthDay.bmp", [1.5, 5], [2.5, 2.5, 2.5])
    model_3 = createModel("resources/models/Dog.obj", "resources/textures/AustralianDog.bmp", "resources/textures/earthDay.bmp", [1.5, 5], [0.75, 0.75, 0.75])
    model_4 = createModel("resources/models/GunS.obj", "resources/textures/handgun_S.bmp", "resources/textures/earthDay.bmp", [0, 5], [2, 2, 2])
    model_5 = createModel("resources/models/Iguana.obj", "resources/textures/Iguana.bmp", "resources/textures/earthDay.bmp", [1, 5], [0.30, 0.30, 0.30])

    model_actual = model_1
    rend.scene.append(model_actual)

    is_running = True

    while is_running:

        keys = pygame.key.get_pressed()
        x, y = pygame.mouse.get_pos()

        # !------------------------------------------------------------------------------------
        # ! --- ENTRADA DE INPUTS POR TECLADO ------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                # ! --- Salir del render Open GL ----------------------------------------------
                if event.key == pygame.K_ESCAPE:
                    is_running = False

                # ! --- Cambiar tipo de renderizado -------------------------------------------
                elif event.key == pygame.K_z:
                    rend.filled_mode()
                elif event.key == pygame.K_x:
                    rend.wireframe_mode()
        # !------------------------------------------------------------------------------------
        all_keyboard_input(keys) # ! El resto de comandos en teclado
        # !------------------------------------------------------------------------------------
        
        # !------------------------------------------------------------------------------------
                            
        delta_time = clock.tick(60) / 1000
        rend.time += delta_time

        rend.update()
        rend.render()
        pygame.display.flip()

    pygame.quit()
