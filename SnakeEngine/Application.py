import webbrowser
import logging

def OpenURL(url: str) -> bool:
    """
    Opens a URL in new tab.
    Opens new browser window if no browser is available.
    Returns: True if successful, False otherwise.
    """
    __logger__ = logging.getLogger("Application")
    __logger__.info("Trying to open URL in default browser: %s...", url)
    browser = webbrowser.open_new_tab(url)
    if browser == False:
        __logger__.error("Failed to open URL: %s", url)
        return False
    else:
        return True