import glfw
from OpenGL.GL import *
from ..Assets.DefaultAssets import DefaultAssets
from ..Rendering.GraphicsContext import GraphicsContext
from ..Rendering.SnakeGLFW import SnakeGLFW
from ..Core.Mathematics.Vector2 import Vector2


class GameWindow:
    def __init__(
        self,
        GraphicsContext: GraphicsContext,
        Size=Vector2(800, 600),
        Title="Snake Engine",
        Icon=DefaultAssets.ENGINE_ICON,
    ):

        self.GraphicsContext = GraphicsContext

        self.Handle = self.GraphicsContext.CreateWindowSurface(
            int(Size.X), int(Size.Y), Title
        )
        self.Width = int(Size.X)
        self.Height = int(Size.Y)

        self._Fullscreen = False
        self._windowed_pos = None
        self._windowed_size = None

        if Icon:
            self.SetIcon(Icon)

    @property
    def Fullscreen(self) -> bool:
        return self._Fullscreen

    @Fullscreen.setter
    def Fullscreen(self, value: bool):
        if value == self._Fullscreen:
            return

        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)

        if not self._Fullscreen:
            self._windowed_pos = glfw.get_window_pos(self.Handle)
            self._windowed_size = (self.Width, self.Height)
            glfw.set_window_monitor(
                self.Handle,
                monitor,
                0,
                0,
                mode.size.width,
                mode.size.height,
                mode.refresh_rate,
            )
            self._Fullscreen = True
        else:
            x, y = self._windowed_pos
            w, h = self._windowed_size
            glfw.set_window_monitor(self.Handle, None, x, y, w, h, 0)
            self._Fullscreen = False

    def SetIcon(self, IconPath: str):
        SnakeGLFW.SetWindowIcon(self.Handle, IconPath)

    def ShouldClose(self) -> bool:
        return glfw.window_should_close(self.Handle)

    def UpdateDimensions(self):
        width, height = glfw.get_framebuffer_size(self.Handle)
        if width > 0 and height > 0:
            self.Width = width
            self.Height = height
            glViewport(0, 0, self.Width, self.Height)
