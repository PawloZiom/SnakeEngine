import math
import numpy as np
from .Vector3 import Vector3


class Matrix4:
    def __init__(self):
        self.M = [0.0] * 16
        self.Identity()

    def Identity(self):
        self.M = [
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        ]

    @staticmethod
    def Perspective(fov_rad, aspect, near, far):
        mat = Matrix4()
        f = 1.0 / math.tan(fov_rad / 2.0)
        mat.M[0] = f / aspect
        mat.M[5] = f
        mat.M[10] = (far + near) / (near - far)
        mat.M[11] = -1.0
        mat.M[14] = (2.0 * far * near) / (near - far)
        mat.M[15] = 0.0
        return mat

    @staticmethod
    def Translate(v: Vector3):
        mat = Matrix4()
        mat.M[12] = v.X
        mat.M[13] = v.Y
        mat.M[14] = v.Z
        return mat

    @staticmethod
    def RotateY(angle_rad):
        mat = Matrix4()
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        mat.M[0] = c
        mat.M[2] = -s
        mat.M[8] = s
        mat.M[10] = c
        return mat

    @staticmethod
    def RotateX(angle_rad):
        mat = Matrix4()
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        mat.M[5] = c
        mat.M[6] = s
        mat.M[9] = -s
        mat.M[10] = c
        return mat

    def Multiply(self, other):
        res = Matrix4()
        for r in range(4):
            for c in range(4):
                val = 0.0
                for i in range(4):
                    val += self.M[i * 4 + r] * other.M[c * 4 + i]
                res.M[c * 4 + r] = val
        return res

    def ToArray(self):
        return np.array(self.M, dtype=np.float32)
