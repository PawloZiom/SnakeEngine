from pathlib import Path
from typing import Optional, Union


class GameSettings:
    def __init__(self):
        self.title: str = "SnakeEngine Game"
        self.company_name: str = "DefaultCompany"
        self.project_name: str = "SnakeGame"

        self.custom_user_data_path: Optional[Union[str, Path]] = None
        self.custom_assets_path: Optional[Union[str, Path]] = None

        self.screen_width: int = 1280
        self.screen_height: int = 720
        self.fullscreen: bool = False
        self.vsync: bool = True
        self.target_fps: int = 60

        self.start_mouse_locked: bool = False
