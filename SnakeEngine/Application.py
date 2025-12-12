import webbrowser

def OpenURL(url: str):
    webbrowser.open(url, 2)

def QuitApp():
    import glfw
    import sys
    import logging
    _logger = logging.getLogger("Engine/Application")
    _logger.info("Quitting application...")
    glfw.terminate()
    _logger.info("GLFW terminated")
    sys.exit()