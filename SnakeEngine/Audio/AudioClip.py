import ctypes
import os
from pathlib import Path
from openal import al

try:
    import pyogg
except ImportError:
    pyogg = None

class AudioClip:
    def __init__(self, filepath: Path):
        self.Filepath = str(filepath)
        self.Duration = 0.0
        self.Loaded = False
        self.Channels = 0
        self.SampleRate = 0
        self.BufferId = None

        self._Load()

    def _Load(self):
        if pyogg is None:
            raise ImportError("PyOgg is not installed.")

        if not os.path.isfile(self.Filepath):
            raise FileNotFoundError(f"File not found: {self.Filepath}")

        ext = os.path.splitext(self.Filepath)[1].lower()

        if ext == ".ogg":
            decoded = pyogg.VorbisFile(self.Filepath)
        elif ext == ".opus":
            decoded = pyogg.OpusFile(self.Filepath)
        elif ext == ".flac":
            decoded = pyogg.FlacFile(self.Filepath)
        elif ext == ".wav":
            decoded = pyogg.WaveFile(self.Filepath)
        else:
            raise ValueError(f"Unsupported audio format: '{ext}'. Supported: .ogg, .opus, .flac, .wav")

        self.Channels = decoded.channels
        self.SampleRate = decoded.frequency

        if self.Channels == 1:
            al_format = al.AL_FORMAT_MONO16
        elif self.Channels == 2:
            al_format = al.AL_FORMAT_STEREO16
        else:
            raise ValueError(f"Unsupported number of channels: {self.Channels} (supported: mono, stereo)")

        buf = ctypes.c_uint(0)

        al.alGenBuffers(1, ctypes.pointer(buf))

        al.alBufferData(
            buf.value,
            al_format,
            decoded.buffer,
            decoded.buffer_length,
            self.SampleRate,
        )

        self.BufferId = buf.value

        bytes_per_sample = 2
        total_samples_per_channel = decoded.buffer_length / bytes_per_sample / self.Channels
        self.Duration = total_samples_per_channel / self.SampleRate if self.SampleRate else 0.0

        self.Loaded = True

    def Unload(self):
        if self.Loaded and self.BufferId is not None:
            buf = ctypes.c_uint(self.BufferId)
            al.alDeleteBuffers(1, ctypes.pointer(buf))

            self.BufferId = None
            self.Loaded = False