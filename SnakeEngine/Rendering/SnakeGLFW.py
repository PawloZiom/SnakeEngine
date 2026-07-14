import glfw
from PIL import Image
import ctypes

from ..Core.Logger import Logger


class SnakeGLFW:
    """
    A cleaner wrapper around GLFW functions for window management and input handling.
    """

    @staticmethod
    def Initialize():
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW.")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    @staticmethod
    def Shutdown():
        glfw.terminate()

    @staticmethod
    def SetWindowIcon(window_handle, image_path: str):
        try:
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            raw_bytes = img.tobytes()

            image = glfw._GLFWimage()
            image.width = width
            image.height = height

            image.pixels = ctypes.cast(
                ctypes.c_char_p(raw_bytes), ctypes.POINTER(ctypes.c_ubyte)
            )

            glfw._glfw.glfwSetWindowIcon(window_handle, 1, ctypes.byref(image))
            Logger.info(f"Window icon set successfully from: {image_path}")
        except Exception as e:
            Logger.error(f"Error occurred while loading icon {image_path}: {e}")

    @staticmethod
    def PollEvents():
        glfw.poll_events()

    @staticmethod
    def GetTime() -> float:
        return glfw.get_time()

    @staticmethod
    def IsKeyPressed(window_handle, key_name: str) -> bool:
        key_map = {
            "ARROW_UP": glfw.KEY_UP,
            "ARROW_DOWN": glfw.KEY_DOWN,
            "ENTER": glfw.KEY_ENTER,
            "ESCAPE": glfw.KEY_ESCAPE,
            "L_ALT": glfw.KEY_LEFT_ALT,
            "R_ALT": glfw.KEY_RIGHT_ALT,
            "SPACE": glfw.KEY_SPACE,
            "W": glfw.KEY_W,
            "A": glfw.KEY_A,
            "S": glfw.KEY_S,
            "D": glfw.KEY_D,
        }

        target_key = key_map.get(key_name.upper())
        if target_key is None:
            return False

        return glfw.get_key(window_handle, target_key) == glfw.PRESS

    @staticmethod
    def GetMousePosition(window_handle) -> tuple:
        return glfw.get_cursor_pos(window_handle)

    @staticmethod
    def IsMouseButtonPressed(window_handle, button_name: str = "LEFT") -> bool:
        button_map = {
            "LEFT": glfw.MOUSE_BUTTON_LEFT,
            "RIGHT": glfw.MOUSE_BUTTON_RIGHT,
            "MIDDLE": glfw.MOUSE_BUTTON_MIDDLE,
        }
        target_button = button_map.get(button_name.upper(), glfw.MOUSE_BUTTON_LEFT)
        return glfw.get_mouse_button(window_handle, target_button) == glfw.PRESS

    @staticmethod
    def SetCursorMode(window_handle, mode: str):
        if mode.upper() == "LOCKED":
            glfw.set_input_mode(window_handle, glfw.CURSOR, glfw.CURSOR_DISABLED)
        else:
            glfw.set_input_mode(window_handle, glfw.CURSOR, glfw.CURSOR_NORMAL)
