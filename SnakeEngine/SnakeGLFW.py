"""
SnakeGLFW is a simple module that handles most of GLFW for Snake Engine.
It provides docstrings to help understand the functions and their usage.
It also includes some error handling.
"""

import glfw
import glfw.GLFW
from enum import Enum

def GetVersion(string: bool = False) -> tuple[int, int, int] | str:
    """
    Returns the version of the GLFW library.
    If `string` is True, it returns the version as a string using glfwGetVersionString function.
    Otherwise, it returns a tuple of (major, minor, revision).
    Using `string` argument is not recommended.
    
    Docs: https://www.glfw.org/docs/3.3/group__init.html#gaa0c1f8b4d6e2c5f7b9d8c0e4f5b6f1a2 (for GetVersion)
    Docs: https://www.glfw.org/docs/3.3/group__init.html#ga026abd003c8e6501981ab1662062f1c0 (for GetVersionString)
    """
    
    if string == False:
        ver = glfw.get_version()
    else:
        ver = glfw.get_version_string()
    return ver

def GetError():
    """
    Returns and clears the last error for the calling thread.
    
    Docs: https://www.glfw.org/docs/3.3/group__init.html#ga944986b4ec0b928d488141f92982aa18
    """
    err = glfw.get_error()
    return err

def Terminate():
    """
    Terminates the GLFW library.
    
    Docs: https://www.glfw.org/docs/3.3/group__init.html#gaaae48c0a18607ea4a4ba951d939f0901
    """
    glfw.terminate()
    
def GetPrimaryMonitor() -> glfw._GLFWmonitor | None:
    """
    Returns the primary monitor.
    Raises an Exception when fails.
    
    Docs: https://www.glfw.org/docs/3.3/group__monitor.html#gac3adb24947eb709e1874028272e5dfc5
    """
    PrimaryMonitor = glfw.get_primary_monitor()
    if not PrimaryMonitor:
        Terminate()
        raise Exception("Failed to get primary monitor")
    else:
        return PrimaryMonitor
    
def GetMonitorWorkarea(monitor: glfw._GLFWmonitor) -> tuple[int, int, int, int] | None:
    """
    returns the position, in screen coordinates, of the upper-left corner of the work area of 
    the specified monitor along with the work area size in screen coordinates.
    
    Docs: https://www.glfw.org/docs/3.3/group__monitor.html#ga7d8bffc6c55539286a6bd20d32a8d7ea
    """
    workarea = glfw.get_monitor_workarea(monitor)
    return workarea
    
    
class WindowPosition(Enum):
    """
    Enum for window position.
    """
    CENTER = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    
class WindowAttribute(Enum):
    """ 
    Enum for window attributes.
    """
    FOCUSED = glfw.FOCUSED
    ICONIFIED = glfw.ICONIFIED
    MAXIMIZED = glfw.MAXIMIZED
    HOVERED = glfw.HOVERED
    VISIBLE = glfw.VISIBLE
    RESIZABLE = glfw.RESIZABLE
    DECORATED = glfw.DECORATED
    AUTO_ICONIFY = glfw.AUTO_ICONIFY
    FLOATING = glfw.FLOATING
    TRANSPARENT_FRAMEBUFFER = glfw.TRANSPARENT_FRAMEBUFFER
    FOCUS_ON_SHOW = glfw.FOCUS_ON_SHOW    
    
def ShowWindow(window: glfw._GLFWwindow):
    """
    Makes the window visible.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#ga61be47917b72536a148300f46494fc66
    """
    glfw.show_window(window)    
    
def HideWindow(window: glfw._GLFWwindow):
    """
    Makes the window invisible.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#ga49401f82a1ba5f15db5590728314d47c
    """
    glfw.hide_window(window)    
    
def SetWindowPosition(window: glfw._GLFWwindow, position: tuple[int, int]):
    """
    Allows to change the window position to any location on the screen.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#ga1abb6d690e8c88e0c8cd1751356dbca8
    """
    glfw.set_window_pos(window, position[0], position[1])

def GetWindowPosition(window: glfw._GLFWwindow) -> tuple[int, int] | None:
    """
    Obtains the current window position on the screen.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#ga73cb526c000876fd8ddf571570fdb634
    """ 
    pos = glfw.get_window_pos(window)
    return pos

def SetWindowAttribute(window: glfw._GLFWwindow, attribute: WindowAttribute, value: bool):
    """
    Sets a window attribute.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#gace2afda29b4116ec012e410a6819033e
    """
    glfw.set_window_attrib(window, attribute.value, glfw.TRUE if value else glfw.FALSE)
    
def DestroyWindow(window: glfw._GLFWwindow):
    """
    Destroys a window and its associated context.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#gacdf43e51376051d2c091662e9fe3d7b2
    """
    glfw.destroy_window(window)

def CreateWindow(size: tuple[int, int] = (640, 480), title: str = "SnakeGLFW Window", monitor: glfw._GLFWmonitor | None = None, share: glfw._GLFWwindow | None = None) -> glfw._GLFWwindow:
    """
    Creates a window and its associated context.
    Raises an Exception when fails.
    
    Docs: https://www.glfw.org/docs/3.3/group__window.html#ga3555a418df92ad53f917597fe2f64aeb
    """  
    CreatedWindow = glfw.create_window(size[0], size[1], title, monitor, share)
    if not CreatedWindow:
        Terminate()
        raise Exception("Failed to create window")
    else:
        return CreatedWindow

def Initialize() -> bool:
    """
    Initializes the GLFW library.
    Raises an Exception when fails.
    
    Docs: https://www.glfw.org/docs/3.3/group__init.html#ga317aac130a235ab08c6db0834907d85e
    """
    print("[SnakeGLFW] Initializing GLFW...")
    glfwVersion = GetVersion()
    print(f"[SnakeGLFW] Using GLFW version: {glfwVersion[0]}.{glfwVersion[1]}.{glfwVersion[2]}")
    
    init = glfw.init()
    if not init:
        Terminate()
        raise Exception("Failed to initialize GLFW!")
    else:
        print("[SnakeGLFW] GLFW initialized.")
        return True
    
