import math
import ctypes
from openal import al

from ..Core.GameScript import GameScript


def _normalize3(x, y, z):
    l = math.sqrt(x * x + y * y + z * z)
    if l < 1e-9:
        return (0.0, 0.0, 1.0)
    return (x / l, y / l, z / l)


def _cross3(ax, ay, az, bx, by, bz):
    return (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)


class AudioListener(GameScript):
    def __init__(self):
        super().__init__()
        self.Volume = 1.0

    def OnActivate(self):
        from .AudioManager import AudioManager
        if AudioManager.Get().ActiveListener is None:
            AudioManager.Get().SetListener(self)

    def OnDeactivate(self):
        from .AudioManager import AudioManager
        mgr = AudioManager.Get()
        if mgr.ActiveListener is self:
            mgr.SetListener(None)

    def OnUpdate(self, delta_time: float):
        from .AudioManager import AudioManager
        manager = AudioManager.Get()

        if manager.ActiveListener is not self or self.Entity is None:
            return

        transform = self.Entity.Transform

        pitch = math.radians(transform.Rotation.X)
        yaw = math.radians(transform.Rotation.Y)

        fx = math.sin(yaw) * math.cos(pitch)
        fy = -math.sin(pitch)
        fz = math.cos(yaw) * math.cos(pitch)
        fx, fy, fz = _normalize3(fx, fy, fz)

        rx, ry, rz = _cross3(fx, fy, fz, 0.0, 1.0, 0.0)
        rx, ry, rz = _normalize3(rx, ry, rz)

        ux, uy, uz = _cross3(rx, ry, rz, fx, fy, fz)

        pos = transform.Position

        al.alListener3f(al.AL_POSITION, pos.X, pos.Y, pos.Z)

        orientation = (ctypes.c_float * 6)(fx, fy, fz, ux, uy, uz)
        al.alListenerfv(al.AL_ORIENTATION, orientation)

        al.alListenerf(al.AL_GAIN, self.Volume * manager.GlobalVolume)