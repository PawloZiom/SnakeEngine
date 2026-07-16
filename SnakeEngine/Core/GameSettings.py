from pathlib import Path
from typing import Optional, Union


class GameSettings:
    def __init__(self):
        self.Title: str = "Snake Engine Game"
        self.CompanyName: str = "DefaultCompany"
        self.ProjectName: str = "SnakeGame"

        self.CustomUserDataPath: Optional[Union[str, Path]] = None
        self.CustomAssetsPath: Optional[Union[str, Path]] = None

        self.WindowWidth: int = 1280
        self.WindowHeight: int = 720
        self.Fullscreen: bool = False
        self.VSync: bool = True
        self.TargetFPS: int = 60
