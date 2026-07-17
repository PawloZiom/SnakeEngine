import pybullet as pb


class PhysicsManager:
    _physics_client = None
    _bodies = []

    @classmethod
    def Initialize(cls, gravity: float = -9.81, fixed_timestep: float = 1.0 / 60.0):
        try:
            cls._physics_client = pb.connect(pb.DIRECT)
            pb.setGravity(0, gravity, 0, physicsClientId=cls._physics_client)
            pb.setPhysicsEngineParameter(
                fixedTimeStep=fixed_timestep, physicsClientId=cls._physics_client
            )
        except Exception:
            pass

    @classmethod
    def Step(cls, delta_time: float):
        if cls._physics_client is None:
            return
        pb.stepSimulation(physicsClientId=cls._physics_client)
        for body in cls._bodies:
            body._SyncToTransform()

    @classmethod
    def RegisterBody(cls, body):
        if body not in cls._bodies:
            cls._bodies.append(body)

    @classmethod
    def UnregisterBody(cls, body):
        if body in cls._bodies:
            cls._bodies.remove(body)

    @classmethod
    def Shutdown(cls):
        if cls._physics_client is not None:
            pb.disconnect(physicsClientId=cls._physics_client)
            cls._physics_client = None
            cls._bodies.clear()
