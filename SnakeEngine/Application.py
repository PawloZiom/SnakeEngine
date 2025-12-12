import webbrowser
import logging
_logger = logging.getLogger("Engine/Application")

def OpenURL(url: str):
    _logger.info(f"Opening URL: {url}")
    webbrowser.open(url, 2)

def QuitApp():
    import glfw
    import sys
    _logger.info("Quitting application...")
    glfw.terminate()
    _logger.info("GLFW terminated")
    sys.exit()