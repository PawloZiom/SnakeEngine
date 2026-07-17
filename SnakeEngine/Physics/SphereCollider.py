import pybullet as pb
from .Collider import Collider


class SphereCollider(Collider):
    def __init__(self, entity, radius: float = 0.5):
        super().__init__(entity)
        self.Radius = radius

        self.shape_id = pb.createCollisionShape(pb.GEOM_SPHERE, radius=self.Radius)