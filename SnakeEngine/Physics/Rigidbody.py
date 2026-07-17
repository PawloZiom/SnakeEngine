import pybullet as pb
from .PhysicsManager import PhysicsManager
from ..Core.Mathematics.Vector3 import Vector3


class RigidBody:
    def __init__(self, entity, mass: float = 1.0, friction: float = 0.5):
        self.entity = entity
        self.mass = mass
        self.friction = friction
        self.bullet_id = None
        self.transform = entity.Transform

        collider = None
        if hasattr(entity, "GetComponent"):
            from SnakeEngine.Physics.Collider import Collider

            collider = entity.GetComponent(Collider)

        if collider and hasattr(collider, "shape_id") and collider.shape_id is not None:
            shape_id = collider.shape_id
        else:
            shape_id = pb.createCollisionShape(pb.GEOM_SPHERE, radius=0.01)

        self._CreateBulletBody(shape_id)
        PhysicsManager.RegisterBody(self)

    def _CreateBulletBody(self, shape_id):
        pos = self.transform.Position
        start_pos = [pos.X, pos.Y, pos.Z]
        start_orientation = [0, 0, 0, 1]

        self.bullet_id = pb.createMultiBody(
            baseMass=self.mass,
            baseCollisionShapeIndex=shape_id,
            basePosition=start_pos,
            baseOrientation=start_orientation,
        )
        pb.changeDynamics(self.bullet_id, -1, lateralFriction=self.friction)

    def ApplyForce(self, force: Vector3):
        if self.bullet_id is not None:
            pb.applyExternalForce(
                self.bullet_id,
                -1,
                [force.X, force.Y, force.Z],
                [0, 0, 0],
                pb.WORLD_FRAME,
            )

    def SetRestitution(self, restitution: float):
        if self.bullet_id is not None:
            pb.changeDynamics(self.bullet_id, -1, restitution=restitution)

    def _SyncToTransform(self):
        if self.bullet_id is None:
            return
        pos, ort = pb.getBasePositionAndOrientation(self.bullet_id)
        self.transform.Position = Vector3(pos[0], pos[1], pos[2])

    def Destroy(self):
        if self.bullet_id is not None:
            pb.removeBody(self.bullet_id)
            self.bullet_id = None
        PhysicsManager.UnregisterBody(self)