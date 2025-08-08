from glfw.GLFW import glfwCreateWindow

class Window:
    def Create(title: str="Snake Engine Window", size: tuple[int, int] = (640, 480)):
        window = glfwCreateWindow(size[0], size[1], title, None, None)
        if not window:
            raise Exception("Failed to create window")
        return window