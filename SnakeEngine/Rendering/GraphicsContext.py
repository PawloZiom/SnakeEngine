import glfw
from OpenGL.GL import *


class GraphicsContext:
    def __init__(self):
        self.PrimaryContextWindow = None

    def CreateWindowSurface(self, width, height, title):
        window_handle = glfw.create_window(width, height, title, None, None)
        if not window_handle:
            raise RuntimeError(f"Failed to create window: {title}")
        if not self.PrimaryContextWindow:
            self.PrimaryContextWindow = window_handle
            glfw.make_context_current(window_handle)
            glEnable(GL_DEPTH_TEST)
            glfw.swap_interval(0)
        return window_handle

    def MakeCurrent(self, window_handle):
        glfw.make_context_current(window_handle)

    def ScreenClear(self, window_handle, r=0.1, g=0.1, b=0.1, a=1.0):
        glfw.make_context_current(window_handle)
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def ScreenPresent(self, window_handle):
        glfw.swap_buffers(window_handle)
