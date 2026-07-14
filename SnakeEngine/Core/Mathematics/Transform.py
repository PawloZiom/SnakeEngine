from .Vector3 import Vector3
from .Matrix4 import Matrix4


class Transform:
    def __init__(self):
        self.Position = Vector3(0.0, 0.0, 0.0)
        self.Rotation = Vector3(0.0, 0.0, 0.0)
        self.Scale = Vector3(1.0, 1.0, 1.0)

    def GetWorldMatrix(self):
        pos_mat = Matrix4.Translate(self.Position)
        rot_y = Matrix4.RotateY(self.Rotation.Y)
        rot_x = Matrix4.RotateX(self.Rotation.X)
        return pos_mat.Multiply(rot_y).Multiply(rot_x)
