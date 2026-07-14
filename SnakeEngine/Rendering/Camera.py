import math
from ..Core.Mathematics.Matrix4 import Matrix4
from ..Core.Mathematics.Transform import Transform


def _normalize3(x, y, z):
    l = math.sqrt(x * x + y * y + z * z)
    if l < 1e-9:
        return (0.0, 0.0, 1.0)
    return (x / l, y / l, z / l)


def _cross3(ax, ay, az, bx, by, bz):
    return (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)


def _dot3(ax, ay, az, bx, by, bz):
    return ax * bx + ay * by + az * bz


class Camera:
    def __init__(self):
        self.Fov = 70.0
        self.Near = 0.1
        self.Far = 1000.0

    def GetViewMatrix(self, entity_transform: Transform) -> Matrix4:
        pitch = math.radians(entity_transform.Rotation.X)
        yaw = math.radians(entity_transform.Rotation.Y)

        fx = math.sin(yaw) * math.cos(pitch)
        fy = -math.sin(pitch)
        fz = math.cos(yaw) * math.cos(pitch)
        fx, fy, fz = _normalize3(fx, fy, fz)

        rx, ry, rz = _cross3(fx, fy, fz, 0.0, 1.0, 0.0)
        rx, ry, rz = _normalize3(rx, ry, rz)

        ux, uy, uz = _cross3(rx, ry, rz, fx, fy, fz)

        px = entity_transform.Position.X
        py = entity_transform.Position.Y
        pz = entity_transform.Position.Z

        m = Matrix4()
        m.M[0] = rx
        m.M[1] = ux
        m.M[2] = -fx
        m.M[3] = 0.0
        m.M[4] = ry
        m.M[5] = uy
        m.M[6] = -fy
        m.M[7] = 0.0
        m.M[8] = rz
        m.M[9] = uz
        m.M[10] = -fz
        m.M[11] = 0.0
        m.M[12] = -_dot3(rx, ry, rz, px, py, pz)
        m.M[13] = -_dot3(ux, uy, uz, px, py, pz)
        m.M[14] = _dot3(fx, fy, fz, px, py, pz)
        m.M[15] = 1.0
        return m
