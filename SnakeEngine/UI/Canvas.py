import os
import sys
import json
import ctypes
from OpenGL.GL import *
import numpy as np
from PIL import Image

from .Button import UIButton
from .Frame import UIFrame
from .Image import UIImage
from .Label import UILabel
from .Slider import UISlider
from .Text import UIText

from ..Assets.DefaultAssets import DefaultAssets
from ..Rendering.ShaderManager import ShaderManager

_SHADER_NAME = "SnakeEngine/UI"


def _ensure_ui_shader():
    if ShaderManager.get(_SHADER_NAME) == 0:
        ShaderManager.load(
            _SHADER_NAME,
            DefaultAssets.UI_SHADER_VERT,
            DefaultAssets.UI_SHADER_FRAG,
        )


class UICanvas:
    def __init__(self):
        self.Vao = glGenVertexArrays(1)
        self.Vbo = glGenBuffers(1)
        self.TextureID = None
        self.Vertices = []

        self.FontCharacters = {}
        self.TextureSize = 512
        self.FontBaseHeight = 32

        _ensure_ui_shader()
        self.ShaderProgram = ShaderManager.get(_SHADER_NAME)

        self.SetupFontAtlas()

    def SetupFontAtlas(self):
        png_path = DefaultAssets.FONT_ATLAS_PNG
        json_path = DefaultAssets.FONT_ATLAS_JSON

        if not os.path.exists(png_path) or not os.path.exists(json_path):
            print(f"BŁĄD: Brak profesjonalnego atlasu czcionek!")
            print(f"Szukano w:\n -> {png_path}\n -> {json_path}")
            print(
                "Wygeneruj pliki narzędziem Pillow i wrzuć do folderu Assets silnika."
            )
            sys.exit(1)

        with open(json_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.TextureSize = meta["texture_size"]
        self.FontBaseHeight = meta["char_height"]
        self.FontCharacters = meta["characters"]

        img = Image.open(png_path)
        self.TextureSize = img.width
        img_data = img.convert("RGBA").tobytes()

        self.TextureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.TextureID)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            self.TextureSize,
            self.TextureSize,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data,
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_2D, 0)

    def PushQuad(self, x, y, w, h, color, u1=0.0, v1=0.0, u2=0.0, v2=0.0):
        r, g, b, a = color
        self.Vertices.extend(
            [
                x, y, u1, v1, r, g, b, a,
                x + w, y, u2, v1, r, g, b, a,
                x + w, y + h, u2, v2, r, g, b, a,
                
                x, y, u1, v1, r, g, b, a,
                x + w, y + h, u2, v2, r, g, b, a,
                x, y + h, u1, v2, r, g, b, a,
            ]
        )

    def PushString(self, text, x, y, scale, color):
        cursor_x = x
        ts = float(self.TextureSize)

        for char in text:
            if char not in self.FontCharacters:
                char = " "

            meta = self.FontCharacters[char]

            w = meta["width"] * scale
            h = meta["height"] * scale

            u_start = meta["x"] / ts
            v_start = meta["y"] / ts
            u_end = (meta["x"] + meta["width"]) / ts
            v_end = (meta["y"] + meta["height"]) / ts

            char_y = y + (self.FontBaseHeight * scale) - h

            self.PushQuad(cursor_x, char_y, w, h, color, u_start, v_start, u_end, v_end)
            cursor_x += meta["advance"] * scale

    def _FlushBatch(self):
        if not self.Vertices:
            return

        data = np.array(self.Vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.Vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
        
        glDrawArrays(GL_TRIANGLES, 0, len(self.Vertices) // 8)
        self.Vertices.clear()

    def Render(self, entities, screen_width, screen_height):
        self.Vertices.clear()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glUseProgram(self.ShaderProgram)
        glUniform2f(
            glGetUniformLocation(self.ShaderProgram, "screenSize"),
            float(screen_width),
            float(screen_height),
        )

        glBindVertexArray(self.Vao)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.TextureID)

        glBindBuffer(GL_ARRAY_BUFFER, self.Vbo)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(16))
        glEnableVertexAttribArray(2)

        for entity in entities:
            frame = entity.GetComponent(UIFrame)
            if frame:
                self.PushQuad(
                    frame.Bounds.Position.X, frame.Bounds.Position.Y,
                    frame.Bounds.Width, frame.Bounds.Height, frame.Color
                )
        self._FlushBatch()

        for entity in entities:
            img = entity.GetComponent(UIImage)
            if img:
                if img.has_texture:
                    self._FlushBatch()
                    
                    glBindTexture(GL_TEXTURE_2D, img.texture_id)
                    
                    glUniform1i(
                        glGetUniformLocation(self.ShaderProgram, "isImage"),
                        1
                    )
                    
                    self.PushQuad(
                        img.Bounds.Position.X, img.Bounds.Position.Y,
                        img.Bounds.Width, img.Bounds.Height, img.Color,
                        0.0, 1.0, 1.0, 0.0
                    )
                    
                    self._FlushBatch()
                    
                    glUniform1i(
                        glGetUniformLocation(self.ShaderProgram, "isImage"),
                        0
                    )
                    
                    glBindTexture(GL_TEXTURE_2D, self.TextureID)
                else:
                    self.PushQuad(
                        img.Bounds.Position.X, img.Bounds.Position.Y,
                        img.Bounds.Width, img.Bounds.Height, img.Color
                    )
                    
        for entity in entities:
            slider = entity.GetComponent(UISlider)
            if slider:
                self.PushQuad(slider.Bounds.Position.X, slider.Bounds.Position.Y, slider.Bounds.Width, slider.Bounds.Height, slider.BackgroundColor)
                fill_w = slider.Bounds.Width * slider.Value
                self.PushQuad(slider.Bounds.Position.X, slider.Bounds.Position.Y, fill_w, slider.Bounds.Height, slider.FillColor)
        self._FlushBatch()

        for entity in entities:
            btn = entity.GetComponent(UIButton)
            if btn:
                render_color = (
                    btn.BackgroundColor[0] * 0.5, btn.BackgroundColor[1] * 0.5,
                    btn.BackgroundColor[2] * 0.5, btn.BackgroundColor[3]
                ) if btn.IsHovered else btn.BackgroundColor

                self.PushQuad(btn.Bounds.Position.X, btn.Bounds.Position.Y, btn.Bounds.Width, btn.Bounds.Height, render_color)
                
                text_scale = 0.5
                total_text_w = sum([self.FontCharacters.get(c, self.FontCharacters[" "])["advance"] for c in btn.Text]) * text_scale
                text_x = btn.Bounds.Position.X + (btn.Bounds.Width - total_text_w) / 2
                text_y = btn.Bounds.Position.Y + (btn.Bounds.Height - (self.FontBaseHeight * text_scale)) / 2
                self.PushString(btn.Text, text_x, text_y, text_scale, btn.TextColor)

        for entity in entities:
            txt = entity.GetComponent(UIText)
            if txt:
                self.PushString(txt.Text, txt.Position.X, txt.Position.Y, txt.Scale, txt.Color)
                
            label = entity.GetComponent(UILabel)
            if label:
                self.PushString(label.Text, label.Position.X, label.Position.Y, label.Scale, label.Color)
                
        self._FlushBatch()

        glBindVertexArray(0)
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)