import ctypes
from openal import al

from ..Core.GameScript import GameScript
from .AudioClip import AudioClip

class AudioSource(GameScript):
    def __init__(self):
        super().__init__()

        self.Clip: AudioClip = None
        self.Loop = False
        self.Volume = 1.0
        self.Pitch = 1.0
        self.PlayOnAwake = False
        self.IsSpatial3D = True

        self.MinDistance = 1.0
        self.MaxDistance = 100.0
        self.RolloffFactor = 1.0

        self._SourceId = None

    def OnStart(self):
        src = ctypes.c_uint(0)

        al.alGenSources(1, ctypes.pointer(src))
        self._SourceId = src.value

        al.alSourcei(
            self._SourceId,
            al.AL_SOURCE_RELATIVE,
            al.AL_FALSE if self.IsSpatial3D else al.AL_TRUE,
        )

        self._ApplyProperties()

        if self.Clip and self.Clip.Loaded:
            al.alSourcei(self._SourceId, al.AL_BUFFER, self.Clip.BufferId)

        if self.PlayOnAwake:
            self.Play()

    def _ApplyProperties(self):
        if self._SourceId is None:
            return

        al.alSourcef(self._SourceId, al.AL_GAIN, self.Volume)
        al.alSourcef(self._SourceId, al.AL_PITCH, self.Pitch)
        al.alSourcei(self._SourceId, al.AL_LOOPING, al.AL_TRUE if self.Loop else al.AL_FALSE)
        al.alSourcef(self._SourceId, al.AL_REFERENCE_DISTANCE, self.MinDistance)
        al.alSourcef(self._SourceId, al.AL_MAX_DISTANCE, self.MaxDistance)
        al.alSourcef(self._SourceId, al.AL_ROLLOFF_FACTOR, self.RolloffFactor)

    def OnUpdate(self, delta_time: float):
        if self._SourceId is None or self.Entity is None:
            return

        self._ApplyProperties()

        pos = self.Entity.Transform.Position
        al.alSource3f(self._SourceId, al.AL_POSITION, pos.X, pos.Y, pos.Z)

    def SetClip(self, clip: AudioClip):
        self.Clip = clip
        if self._SourceId is not None and clip and clip.Loaded:
            self.Stop()
            al.alSourcei(self._SourceId, al.AL_BUFFER, clip.BufferId)

    def Play(self):
        if self._SourceId is not None and self.Clip and self.Clip.Loaded:
            al.alSourcePlay(self._SourceId)

    def Pause(self):
        if self._SourceId is not None:
            al.alSourcePause(self._SourceId)

    def Stop(self):
        if self._SourceId is not None:
            al.alSourceStop(self._SourceId)

    def IsPlaying(self) -> bool:
        if self._SourceId is None:
            return False
        state = ctypes.c_int(0)
        al.alGetSourcei(self._SourceId, al.AL_SOURCE_STATE, ctypes.byref(state))
        return state.value == al.AL_PLAYING

    def OnDeactivate(self):
        self.Stop()

    def ReleaseNative(self):
        if self._SourceId is not None:
            src = ctypes.c_uint(self._SourceId)
            al.alDeleteSources(1, ctypes.pointer(src))
            self._SourceId = None