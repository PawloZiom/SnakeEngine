import glfw

class Window:
    """GLFW Window wrapper for Snake Engine"""
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "Snake Engine"):
        """
        Initialize window
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
        """
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self.is_running = False
    
    def create(self) -> bool:
        """
        Create GLFW window
        
        Returns:
            True if successful, False otherwise
        """
        # Initialize GLFW
        if not glfw.init():
            print("ERROR: Failed to initialize GLFW")
            return False
        
        # Create window
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        
        if not self.window:
            print("ERROR: Failed to create GLFW window")
            glfw.terminate()
            return False
        
        # Make context current
        glfw.make_context_current(self.window)
        
        # Set key callback for ESC to close
        glfw.set_key_callback(self.window, self._key_callback)
        
        self.is_running = True
        print(f"✓ Window created: {self.width}x{self.height}")
        
        return True
    
    def should_close(self) -> bool:
        """Check if window should close"""
        if not self.window:
            return True
        return glfw.window_should_close(self.window)
    
    def update(self) -> None:
        """Update window (swap buffers and poll events)"""
        if self.window:
            glfw.swap_buffers(self.window)
            glfw.poll_events()
    
    def destroy(self) -> None:
        """Destroy window and cleanup"""
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()
        self.is_running = False
        print("✓ Window destroyed")
    
    def _key_callback(self, window, key, scancode, action, mods):
        """Internal key callback - ESC closes window"""
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)