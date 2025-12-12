import glfw
import logging

class Window():
    def __init__(self, width: int = 1780, height: int = 720, title: str = "Snake Engine Window"):
        _logger = logging.getLogger("Engine/Window")
        
        self.width = width
        self.height = height

        self.window = glfw.create_window(self.width, self.height, title, None, None)
        
        if self.window:
            _logger.info(f'Created window: "{title}" with size {self.width}x{self.height}.')

        glfw.set_window_pos(self.window, 400, 200)
        glfw.make_context_current(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def poll_events(self):
        glfw.poll_events()

    def terminate(self):
        glfw.terminate()