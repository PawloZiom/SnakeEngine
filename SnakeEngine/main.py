import SnakeGLFW
import logging

from pathlib import Path
from time import sleep
from platform import python_version, system, version as system_version
from sys import exit

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s::%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S"
)

class SnakeEngine:
    def __init__(self):
        engine_logger = logging.getLogger("EngineMain")
        
        from importlib.metadata import version, packages_distributions
        from os import system as command
        
        command('cls' if system() == 'Windows' else 'clear')
        ver = version('SnakeEngine') if 'SnakeEngine' in packages_distributions() else 'Unknown version'
        engine_logger.info(f"Snake Engine: {ver}")
        engine_logger.info(f"Running on {system()} {system_version()}")
        engine_logger.info(f"Using Python {python_version()}")
        del version, packages_distributions, command
        
        SnakeGLFW.Initialize()
        engine_logger.info("Showing splash screen...")
        self.__ShowSplashScreen()
        
        self.GameLogger = logging.getLogger("Game")
    
    def __ShowSplashScreen(self):
        from PIL import Image
        from OpenGL import GL
        
        monitorWorkarea = SnakeGLFW.GetMonitorWorkarea(SnakeGLFW.GetPrimaryMonitor())
        center_pos = ((monitorWorkarea[2] - 900) // 2, (monitorWorkarea[3] - 400) // 2)
        
        SnakeGLFW.SetWindowHint(SnakeGLFW.WindowHint.TRANSPARENT_FRAMEBUFFER, True)
        self.__splash__ = SnakeGLFW.CreateWindow(size=(900, 400), title="Snake Engine")
        SnakeGLFW.MakeCurrentContext(self.__splash__)
        SnakeGLFW.SetWindowPosition(self.__splash__, center_pos)
        SnakeGLFW.SetWindowAttribute(self.__splash__, SnakeGLFW.WindowAttribute.RESIZABLE, False)
        SnakeGLFW.SetWindowAttribute(self.__splash__, SnakeGLFW.WindowAttribute.DECORATED, False)
                
        splash_img = Image.open(Path(__file__).parent / "engineAssets" / "SnakeEngineSplashScreen.png").transpose(Image.FLIP_TOP_BOTTOM)
        splash_imgData = splash_img.convert("RGBA").tobytes()
        splash_texture = GL.glGenTextures(1)
        
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, splash_texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, splash_img.size[0], splash_img.size[1], 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, splash_imgData)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBindTexture(GL.GL_TEXTURE_2D, splash_texture)
        
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0, 0); GL.glVertex2f(-1, -1)
        GL.glTexCoord2f(1, 0); GL.glVertex2f(1, -1)
        GL.glTexCoord2f(1, 1); GL.glVertex2f(1, 1)
        GL.glTexCoord2f(0, 1); GL.glVertex2f(-1, 1)
        GL.glEnd()
        
        SnakeGLFW.SwapBuffers(self.__splash__) 
        SnakeGLFW.SetWindowHint(SnakeGLFW.WindowHint.TRANSPARENT_FRAMEBUFFER, False)     
        
        sleep(2)  
            
    def Run(self):
        """
        Starts the main game loop.
        """
        engine_logger = logging.getLogger("EngineMain")
        self.GameWindow = SnakeGLFW.CreateWindow(size=(640, 480), title="GameWindow")
        engine_logger.info("Game Window have been created")
        
        if hasattr(self, "__splash__"):
            SnakeGLFW.DestroyWindow(self.__splash__)
            del self.__splash__
        
        while not SnakeGLFW.WindowShouldClose(self.GameWindow):
            SnakeGLFW.PoolEvents()
            SnakeGLFW.SwapBuffers(self.GameWindow)
            
        self.RequestExit()
            
    def RequestExit(self, error_code: int = None):
        """
        Requests the engine to exit.
        """
        engine_logger = logging.getLogger("EngineMain")
        if error_code is None:
            engine_logger.info("Game requested to exit")
        else:
            engine_logger.info("Game requested to exit with error code: %d", error_code)
        
        SnakeGLFW.Terminate()
        exit()
        
if __name__ == "__main__":
    Engine = SnakeEngine()
    Engine.Run()