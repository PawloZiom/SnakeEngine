from .AudioDevice import AudioDevice
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

    def Initialize(self, device_name: str = None):
        AudioDevice.Get().Initialize(device_name)

    def Shutdown(self):
        AudioDevice.Get().Shutdown()

    def SetListener(self, listener: AudioListener):
        self.ActiveListener = listener
