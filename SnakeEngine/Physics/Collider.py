from ..Core.Mathematics.Vector3 import Vector3


class Collider:
    def __init__(self, entity):
        self.entity = entity
        self.Offset = Vector3(0, 0, 0)
        self.IsTrigger = False
        self.shape_id = None
