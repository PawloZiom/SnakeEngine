from ..Core.Mathematics.Vector3 import Vector3
from .AudioListener import AudioListener


class AudioManager:

    _instance = None

    @classmethod
    def Get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.GlobalVolume = 1.0
        self.ActiveListener = None

    def SetListener(self, listener: AudioListener):
        self.ActiveListener = listener