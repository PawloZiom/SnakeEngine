import os
import ctypes
from OpenGL.GL import *
import numpy as np

from ..Assets.DefaultAssets import DefaultAssets
from .ShaderManager import ShaderManager

_SHADER_NAME = "SnakeEngine/Skybox"


def _ensure_skybox_shader():
    if ShaderManager.get(_SHADER_NAME) == 0:
        ShaderManager.load(
            _SHADER_NAME,
            DefaultAssets.SKYBOX_SHADER_VERT,
            DefaultAssets.SKYBOX_SHADER_FRAG,
        )


class Skybox:
    def __init__(self):
        self.CubemapTextureID = 0
        self.CubemapPaths = []
        self.Enabled = True

        self._vao = 0
        self._vbo = 0

        self._init_geometry()
        _ensure_skybox_shader()

    def _init_geometry(self):
        vertices = np.array(
            [
                -1.0,
                1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                -1.0,
                -1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
            ],
            dtype=np.float32,
        )

        self._vao = glGenVertexArrays(1)
        self._vbo = glGenBuffers(1)

        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0)
        )
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def LoadCubemap(self, paths: list):
        self.CubemapPaths = paths

        try:
            from PIL import Image
        except ImportError:
            print("[Skybox] Zainstaluj Pillow żeby wczytywać cubemapy.")
            return

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, tex_id)

        faces = [
            GL_TEXTURE_CUBE_MAP_POSITIVE_X,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
        ]

        for i, path in enumerate(paths):
            if not os.path.exists(path):
                print(f"[Skybox] Brak pliku: {path}")
                glDeleteTextures(1, [tex_id])
                return
            try:
                img = Image.open(path).convert("RGBA")
                img_data = img.tobytes()
                glTexImage2D(
                    faces[i],
                    0,
                    GL_RGBA,
                    img.width,
                    img.height,
                    0,
                    GL_RGBA,
                    GL_UNSIGNED_BYTE,
                    img_data,
                )
            except Exception as e:
                print(f"[Skybox] Błąd ładowania {path}: {e}")
                glDeleteTextures(1, [tex_id])
                return

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        for wrap in (GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_WRAP_R):
            glTexParameteri(GL_TEXTURE_CUBE_MAP, wrap, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

        self.CubemapTextureID = tex_id
        print(f"[Skybox] Cubemapa załadowana ({len(paths)} twarzy).")

    def Render(self, projection_matrix, view_matrix):
        if not self.Enabled:
            return

        program = ShaderManager.get(_SHADER_NAME)
        if not program:
            return

        cull_on = glIsEnabled(GL_CULL_FACE)
        depth_on = glIsEnabled(GL_DEPTH_TEST)

        if cull_on:
            glDisable(GL_CULL_FACE)
        if not depth_on:
            glEnable(GL_DEPTH_TEST)

        glDepthMask(GL_FALSE)
        glDepthFunc(GL_LEQUAL)

        glUseProgram(program)
        glUniformMatrix4fv(
            glGetUniformLocation(program, "projection"),
            1,
            GL_FALSE,
            projection_matrix.ToArray(),
        )
        glUniformMatrix4fv(
            glGetUniformLocation(program, "view"), 1, GL_FALSE, view_matrix.ToArray()
        )

        if self.CubemapTextureID > 0:
            glUniform1i(glGetUniformLocation(program, "use_fallback"), GL_FALSE)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_CUBE_MAP, self.CubemapTextureID)
            glUniform1i(glGetUniformLocation(program, "skybox"), 0)
        else:
            glUniform1i(glGetUniformLocation(program, "use_fallback"), GL_TRUE)

        glBindVertexArray(self._vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)

        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
        if not depth_on:
            glDisable(GL_DEPTH_TEST)
        if cull_on:
            glEnable(GL_CULL_FACE)
        glUseProgram(0)
