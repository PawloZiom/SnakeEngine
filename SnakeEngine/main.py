from window import Window
from glfw.GLFW import glfwInit

class SnakeEngine:
    
    def __init__(self):
        if not glfwInit():
            raise Exception("Failed to initialize GLFW")