from openal import alc
from ..Core.Logger import Logger


class AudioDevice:
    _instance = None

    @classmethod
    def Get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._device = None
        self._context = None
        self.IsInitialized = False

    def Initialize(self, device_name: str = None):
        if self.IsInitialized:
            return

        self._device = alc.alcOpenDevice(device_name.encode() if device_name else None)
        if not self._device:
            raise RuntimeError(
                "Could not open audio device (OpenAL). Check if OpenAL drivers are available (e.g., OpenAL Soft)."
            )

        self._context = alc.alcCreateContext(self._device, None)
        if not self._context:
            alc.alcCloseDevice(self._device)
            self._device = None
            raise RuntimeError("Could not create OpenAL context.")

        alc.alcMakeContextCurrent(self._context)
        self.IsInitialized = True
        Logger.info(
            "Audio system initialized. Using device: "
            + alc.alcGetString(self._device, alc.ALC_DEVICE_SPECIFIER).decode()
        )

    def Shutdown(self):
        if not self.IsInitialized:
            return

        alc.alcMakeContextCurrent(None)

        if self._context:
            alc.alcDestroyContext(self._context)
            self._context = None

        if self._device:
            alc.alcCloseDevice(self._device)
            self._device = None

        self.IsInitialized = False
