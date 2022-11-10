import glm #pip install PyGLM

from numpy import array, float32

# pip install PyOpenGL
from OpenGL.GL import *

from Obj import Obj

from pygame import image

class Model(object):
    def __init__(self, objName, textureName):
        self.model = Obj(objName)

        self.createVertexBuffer()

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

        self.textureSurface = image.load(textureName)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)


    def createVertexBuffer(self):
        buffer = []

        self.polycount = 0

        for face in self.model.faces:
            self.polycount += 1

            for i in range(3):
                # positions
                pos = self.model.vertices[face[i][0] - 1]
                buffer.append(pos[0])
                buffer.append(pos[1])
                buffer.append(pos[2])

                # texcoords
                uvs = self.model.texcoords[face[i][1] - 1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])

                # normals
                norm = self.model.normals[face[i][2] - 1]
                buffer.append(norm[0])
                buffer.append(norm[1])
                buffer.append(norm[2])

            if len(face) == 4:

                self.polycount += 1

                for i in [0,2,3]:
                    # positions
                    pos = self.model.vertices[face[i][0] - 1]
                    buffer.append(pos[0])
                    buffer.append(pos[1])
                    buffer.append(pos[2])

                    # texcoords
                    uvs = self.model.texcoords[face[i][1] - 1]
                    buffer.append(uvs[0])
                    buffer.append(uvs[1])

                    # normals
                    norm = self.model.normals[face[i][2] - 1]
                    buffer.append(norm[0])
                    buffer.append(norm[1])
                    buffer.append(norm[2])


        self.vertBuffer = array(buffer, dtype = float32)
        
        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

    def get_model_matrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def render(self):

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Mandar la informacion de vertices
        glBufferData(GL_ARRAY_BUFFER,           # Buffer ID
                     self.vertBuffer.nbytes,    # Buffer size in bytes
                     self.vertBuffer,           # Buffer data
                     GL_STATIC_DRAW)            # Usage

        # Atributos

        # Atributo de posiciones
        glVertexAttribPointer(0,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 8,            # Stride
                              ctypes.c_void_p(0))# Offset

        glEnableVertexAttribArray(0)

        # Atributo de texcoords
        glVertexAttribPointer(1,                # Attribute number
                              2,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 8,            # Stride
                              ctypes.c_void_p(4*3))# Offset

        glEnableVertexAttribArray(1)

        # Atributo de normals
        glVertexAttribPointer(2,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 8,            # Stride
                              ctypes.c_void_p(4*5))# Offset

        glEnableVertexAttribArray(2)


        # Dar la textura
        glActiveTexture( GL_TEXTURE0 )
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D,                     # Texture Type
                     0,                                 # Positions
                     GL_RGB,                            # Format
                     self.textureSurface.get_width(),   # Width
                     self.textureSurface.get_height(),  # Height
                     0,                                 # Border
                     GL_RGB,                            # Format
                     GL_UNSIGNED_BYTE,                  # Type
                     self.textureData)                  # Data

        glGenerateMipmap(GL_TEXTURE_2D)



        glDrawArrays(GL_TRIANGLES, 0, self.polycount * 3 )