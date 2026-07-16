from typing import Optional, Tuple
from OpenGL.GL import *
from PIL import Image
import io

from .Extent import UIExtent
from ..Core.FileSystem import FileSystem
from ..Core.Logger import Logger


class UIImage:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        path: Optional[str] = None,
    ):
        self.Bounds = UIExtent(x, y, width, height)
        self.Color = color
        self._path: Optional[str] = None
        self._texture_id: int = 0

        if path:
            self.path = path

    @property
    def path(self) -> Optional[str]:
        return self._path

    @path.setter
    def path(self, new_path: str):
        if self._path == new_path:
            return

        self._path = new_path
        self._load_texture()

    @property
    def texture_id(self) -> int:
        return self._texture_id

    @property
    def has_texture(self) -> bool:
        return self._texture_id > 0

    def _load_texture(self):
        self._cleanup_texture()

        if not self._path:
            return

        Logger.info(f"Loading UI image texture: '{self._path}'")

        img_bytes = None
        if FileSystem.asset_exists(self._path):
            img_bytes = FileSystem.read_asset_bytes(self._path)
        elif FileSystem.exists(self._path):
            img_bytes = FileSystem.read_bytes(self._path)

        if not img_bytes:
            Logger.error(f"UI Image source file not found: '{self._path}'")
            return

        try:
            img = Image.open(io.BytesIO(img_bytes))
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

            if img.mode != "RGBA":
                img = img.convert("RGBA")

            img_data = img.tobytes("raw", "RGBA")
            width, height = img.size
        except Exception as e:
            Logger.error(
                f"Failed to parse image file '{self._path}' via Pillow: {e}",
                exc_info=True,
            )
            return

        try:
            self._texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self._texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                width,
                height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                img_data,
            )

            glBindTexture(GL_TEXTURE_2D, 0)
            Logger.info(
                f"Successfully uploaded UI texture '{self._path}' to GPU (ID: {self._texture_id}, Resolution: {width}x{height})"
            )
        except Exception as e:
            Logger.error(
                f"Failed to upload UI texture '{self._path}' to OpenGL: {e}",
                exc_info=True,
            )
            self._cleanup_texture()

    def _cleanup_texture(self):
        if self._texture_id > 0:
            try:
                from OpenGL.GL import glDeleteTextures
                import sys

                if sys and sys.meta_path is not None:
                    glDeleteTextures(int(self._texture_id))
            except Exception as e:
                pass
            self._texture_id = 0

    def cleanup(self):
        self._cleanup_texture()

    def __del__(self):
        pass
