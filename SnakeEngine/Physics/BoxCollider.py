from .Collider import Collider
from ..Core.Mathematics.Vector3 import Vector3


class BoxCollider(Collider):

    def __init__(self, entity):
        super().__init__(entity)
        self.Size = Vector3(1.0, 1.0, 1.0)
