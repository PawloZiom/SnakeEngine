import pybullet as pb
from .Collider import Collider
from ..Core.Mathematics.Vector3 import Vector3


class BoxCollider(Collider):
    def __init__(self, entity, size: Vector3 = None):
        super().__init__(entity)
        self.Size = size if size is not None else Vector3(1.0, 1.0, 1.0)

        half_extents = [self.Size.X / 2.0, self.Size.Y / 2.0, self.Size.Z / 2.0]
        self.shape_id = pb.createCollisionShape(pb.GEOM_BOX, halfExtents=half_extents)