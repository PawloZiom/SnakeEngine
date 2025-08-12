from pathlib import Path
from time import sleep
from platform import python_version, system, version as system_version

import SnakeGLFW

class SnakeEngine():
    def __init__(self):
        from os import system as command
        command('cls' if system()=='Windows' else 'clear')
        
        
        from importlib.metadata import version, packages_distributions
        ver = version('SnakeEngine') if 'SnakeEngine' in packages_distributions() else 'Unknown version'
        
        print(f"Snake Engine: {ver}")
        print(f"Running on {system()} {system_version()}")
        print(f"Using Python {python_version()}")
        print("")
        
        SnakeGLFW.Initialize()
        monitorWorkarea = SnakeGLFW.GetMonitorWorkarea(SnakeGLFW.GetPrimaryMonitor())
        center_pos = ((monitorWorkarea[2] - 900) // 2, (monitorWorkarea[3] - 400) // 2)
        
        splash = SnakeGLFW.CreateWindow(size=(900, 400), title="Snake Engine")
        SnakeGLFW.SetWindowPosition(splash, center_pos)
        SnakeGLFW.SetWindowAttribute(splash, SnakeGLFW.WindowAttribute.RESIZABLE, False)
        SnakeGLFW.SetWindowAttribute(splash, SnakeGLFW.WindowAttribute.DECORATED, False)
        
        sleep(1)  # Simulate some processing time
        SnakeGLFW.Terminate()
        
    def run(self):
        """
        
        """
        pass
        
if __name__ == "__main__":
    game = SnakeEngine()
    game.run()
    