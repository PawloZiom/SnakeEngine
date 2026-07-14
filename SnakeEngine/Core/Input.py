class Input:
    _window_handle = None
    _snake_glfw = None

    _mouse_x = 0.0
    _mouse_y = 0.0
    _mouse_delta_x = 0.0
    _mouse_delta_y = 0.0
    _first_mouse_frame = True

    @classmethod
    def _Initialize(cls, window_handle, snake_glfw):
        cls._window_handle = window_handle
        cls._snake_glfw = snake_glfw

    @classmethod
    def _UpdateStates(cls):
        if not cls._window_handle or not cls._snake_glfw:
            return

        new_x, new_y = cls._snake_glfw.GetMousePosition(cls._window_handle)

        if cls._first_mouse_frame:
            cls._mouse_x = new_x
            cls._mouse_y = new_y
            cls._first_mouse_frame = False

        cls._mouse_delta_x = new_x - cls._mouse_x
        cls._mouse_delta_y = new_y - cls._mouse_y

        cls._mouse_x = new_x
        cls._mouse_y = new_y

    @classmethod
    def IsKeyPressed(cls, key_name: str) -> bool:
        if not cls._window_handle:
            return False
        return cls._snake_glfw.IsKeyPressed(cls._window_handle, key_name)

    @classmethod
    def IsMouseButtonPressed(cls, button_name: str) -> bool:
        if not cls._window_handle:
            return False
        return cls._snake_glfw.IsMouseButtonPressed(cls._window_handle, button_name)

    @classmethod
    def GetMousePosition(cls):
        return cls._mouse_x, cls._mouse_y

    @classmethod
    def GetMouseDelta(cls):
        return cls._mouse_delta_x, cls._mouse_delta_y
