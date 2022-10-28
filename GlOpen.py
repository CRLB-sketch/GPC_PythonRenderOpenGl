"""
Tomar en cuenta los angulos de euler
"""

import glm # pip install PyGLM

from numpy import array, float32

# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Buffer(object):
    def __init__(self, data) -> None:
        self.data = data
        self.create_vertex_buffer()

    def create_vertex_buffer(self):
        self.vert_buffer = array(self.data, dtype = float32)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

    def render(self):        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Mandar la informacion de vertices
        glBufferData(GL_ARRAY_BUFFER,           # Buffer ID
                     self.vert_buffer.nbytes,    # Buffer size in bytes
                     self.vert_buffer,           # Buffer data
                     GL_STATIC_DRAW)            # Usage

        # Atributos

        # Atributo de posiciones
        glVertexAttribPointer(0,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 6,            # Stride
                              ctypes.c_void_p(0))# Offset

        glEnableVertexAttribArray(0)

        # Atributo de color
        glVertexAttribPointer(1,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 6,            # Stride
                              ctypes.c_void_p(4*3))# Offset

        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vert_buffer) / 6) )

class Renderer(object):
    def __init__(self, screen) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        # ! Tomar en cuenta el tema de flags
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.scene = []
        self.active_shader = None
        
        # ViewMatrix
        self.cam_position = glm.vec3(0,0,0)
        self.cam_rotation = glm.vec3(0,0,0)
        self.view_matrix = self.get_view_matrix()

        # Projection Matrix
        self.projectionMatrix = glm.perspective(
            glm.radians(60),        # FOV
            self.width/self.height, # Aspect Ratio
            0.1,                    # Near Plane
            1000 # Far Plane
        )                   
        
    def get_view_matrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.cam_position)

        pitch = glm.rotate(identity, glm.radians(self.cam_rotation.x), glm.vec3(1,0,0))
        yaw   = glm.rotate(identity, glm.radians(self.cam_rotation.y), glm.vec3(0,1,0))
        roll  = glm.rotate(identity, glm.radians(self.cam_rotation.z), glm.vec3(0,0,1))

        rotationMat = pitch * yaw * roll

        camMatrix = translateMat * rotationMat

        return glm.inverse(camMatrix)

    def set_shaders(self, vertex_shader, fragment_shader):
        if vertex_shader is not None and fragment_shader is not None:
            self.active_shader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            )
        else:
            self.active_shader = None
            
    def update(self):
        self.view_matrix = self.get_view_matrix()

    def render(self) -> None:
        # alfa es transparencia :v
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Borrar el color y profundidad del bit

        if self.active_shader is not None:
            glUseProgram(self.active_shader)

        for obj in self.scene:
            obj.render()