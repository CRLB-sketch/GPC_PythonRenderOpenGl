# Esta clase se llama gl
import glm # pip install PyGLM

# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# from OpenGL.GLUT import *
# from OpenGL.GLU import *

class Renderer(object):
    def __init__(self, screen) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        # ! Tomar en cuenta el tema de flags
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

    def render(self) -> None:
        # alfa es transparencia :v
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Borrar el color y profundidad del bit