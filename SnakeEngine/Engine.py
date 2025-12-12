from .Window import Window
from .Application import QuitApp
from time import sleep
import platform
import logging
import glfw
from . import version, credits

class SnakeEngine():
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(name)s(%(levelname)s)] %(message)s',
            datefmt='%H:%M:%S'
        )
        
        self._engine_logger = logging.getLogger("Engine")
        
    def Start(self):
        print('=' * 40)
        print(f'🐍 Snake Engine (ver. {str(version)})')
        print(f'Running on Python {str(platform.python_version())}')
        credits_full = ""
        for name in credits:
            if name == list(credits)[-1]:
                credits_full += name
            else:
                credits_full += name + ", "
            
        print(f'Developed by {credits_full}')
        print('=' * 40 + '\n')

        self._engine_logger.info('Initializing GLFW, please wait...')
        if not glfw.init():
            self._engine_logger.error('Failed to initialize GLFW.')
            return
        else:
            ver = glfw.get_version()
            self._engine_logger.info(f'GLFW initialized. Version {ver[0]}.{ver[1]}.{ver[2]}')

        window = Window(1280, 720, "Snake Engine Window")
        
        self._engine_logger.info('Game loop started')
        
        isRunning = True
        while not window.should_close() and isRunning:
            glfw.poll_events()
            window.swap_buffers()
            sleep(1 / 60)  # Simulate ~60 FPS
        
        QuitApp()
        
        
        