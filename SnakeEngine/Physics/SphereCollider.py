from .Collider import Collider


class SphereCollider(Collider):

    def __init__(self, entity):
        super().__init__(entity)
        self.Radius = 0.5
