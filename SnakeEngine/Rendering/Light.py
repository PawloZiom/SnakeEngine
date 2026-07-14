from ..Core.GameEntity import GameEntity
from ..Core.Mathematics.Vector3 import Vector3


class Light:
    DIRECTIONAL = 0
    POINT = 1
    AMBIENT = 2

    def __init__(self):
        self.Type = Light.DIRECTIONAL
        self.Color = Vector3(1.0, 1.0, 1.0)
        self.Intensity = 1.0

        self.Range = 10.0
        self.Attenuation = Vector3(1.0, 0.09, 0.032)
