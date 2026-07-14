import ctypes
from OpenGL.GL import *
import numpy as np

from ..Core.Mathematics.Matrix4 import Matrix4
from ..Core.Mathematics.Transform import Transform
from ..Assets.DefaultAssets import DefaultAssets
from .ShaderManager import ShaderManager

_SHADER_NAME = "SnakeEngine/Default"


def _ensure_default_shader():
    if ShaderManager.get(_SHADER_NAME) == 0:
        ShaderManager.load(
            _SHADER_NAME,
            DefaultAssets.SHADER_VERT,
            DefaultAssets.SHADER_FRAG,
        )


class MeshRenderer:
    def __init__(self):
        self.Vao = None
        self.Vbo = None
        self.VertexCount = 0
        self._shader_name = _SHADER_NAME
        self._InitializeCube()

    def _InitializeCube(self):
        _ensure_default_shader()

        vertices = [
            -0.5,
            -0.5,
            0.5,
            1.0,
            0.0,
            0.0,
            0.5,
            -0.5,
            0.5,
            1.0,
            0.0,
            0.0,
            0.5,
            0.5,
            0.5,
            1.0,
            0.0,
            0.0,
            -0.5,
            -0.5,
            0.5,
            1.0,
            0.0,
            0.0,
            0.5,
            0.5,
            0.5,
            1.0,
            0.0,
            0.0,
            -0.5,
            0.5,
            0.5,
            1.0,
            0.0,
            0.0,
            -0.5,
            -0.5,
            -0.5,
            0.0,
            1.0,
            0.0,
            -0.5,
            0.5,
            -0.5,
            0.0,
            1.0,
            0.0,
            0.5,
            0.5,
            -0.5,
            0.0,
            1.0,
            0.0,
            -0.5,
            -0.5,
            -0.5,
            0.0,
            1.0,
            0.0,
            0.5,
            0.5,
            -0.5,
            0.0,
            1.0,
            0.0,
            0.5,
            -0.5,
            -0.5,
            0.0,
            1.0,
            0.0,
            -0.5,
            0.5,
            -0.5,
            0.0,
            0.0,
            1.0,
            -0.5,
            0.5,
            0.5,
            0.0,
            0.0,
            1.0,
            0.5,
            0.5,
            0.5,
            0.0,
            0.0,
            1.0,
            -0.5,
            0.5,
            -0.5,
            0.0,
            0.0,
            1.0,
            0.5,
            0.5,
            0.5,
            0.0,
            0.0,
            1.0,
            0.5,
            0.5,
            -0.5,
            0.0,
            0.0,
            1.0,
            -0.5,
            -0.5,
            -0.5,
            1.0,
            1.0,
            0.0,
            0.5,
            -0.5,
            -0.5,
            1.0,
            1.0,
            0.0,
            0.5,
            -0.5,
            0.5,
            1.0,
            1.0,
            0.0,
            -0.5,
            -0.5,
            -0.5,
            1.0,
            1.0,
            0.0,
            0.5,
            -0.5,
            0.5,
            1.0,
            1.0,
            0.0,
            -0.5,
            -0.5,
            0.5,
            1.0,
            1.0,
            0.0,
            0.5,
            -0.5,
            -0.5,
            1.0,
            0.0,
            1.0,
            0.5,
            0.5,
            -0.5,
            1.0,
            0.0,
            1.0,
            0.5,
            0.5,
            0.5,
            1.0,
            0.0,
            1.0,
            0.5,
            -0.5,
            -0.5,
            1.0,
            0.0,
            1.0,
            0.5,
            0.5,
            0.5,
            1.0,
            0.0,
            1.0,
            0.5,
            -0.5,
            0.5,
            1.0,
            0.0,
            1.0,
            -0.5,
            -0.5,
            -0.5,
            0.0,
            1.0,
            1.0,
            -0.5,
            -0.5,
            0.5,
            0.0,
            1.0,
            1.0,
            -0.5,
            0.5,
            0.5,
            0.0,
            1.0,
            1.0,
            -0.5,
            -0.5,
            -0.5,
            0.0,
            1.0,
            1.0,
            -0.5,
            0.5,
            0.5,
            0.0,
            1.0,
            1.0,
            -0.5,
            0.5,
            -0.5,
            0.0,
            1.0,
            1.0,
        ]

        data = np.array(vertices, dtype=np.float32)
        self.VertexCount = len(vertices) // 6

        self.Vao = glGenVertexArrays(1)
        self.Vbo = glGenBuffers(1)

        glBindVertexArray(self.Vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.Vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

        stride = 6 * 4
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @property
    def ShaderProgram(self) -> int:
        return ShaderManager.get(self._shader_name)

    def use_shader(self, name: str):
        self._shader_name = name

    def Render(self, transform: Transform, view_mat: Matrix4, proj_mat: Matrix4):
        program = self.ShaderProgram
        if not program:
            return

        glUseProgram(program)

        model_loc = glGetUniformLocation(program, "model")
        view_loc = glGetUniformLocation(program, "view")
        proj_loc = glGetUniformLocation(program, "projection")

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, transform.GetWorldMatrix().M)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_mat.M)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, proj_mat.M)

        glBindVertexArray(self.Vao)
        glDrawArrays(GL_TRIANGLES, 0, self.VertexCount)
        glBindVertexArray(0)
