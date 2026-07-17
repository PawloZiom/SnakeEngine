import uuid

from .Mathematics.Transform import Transform
from .GameScript import GameScript


class GameEntity:
    def __init__(self):
        self.Uid = str(uuid.uuid4())
        self._Name = "Entity"
        self.Transform = Transform()
        self.Components = {}
        self._IsActive = True

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, value):
        self._Name = value

    @property
    def IsActive(self):
        return self._IsActive

    def Activate(self):
        if not self._IsActive:
            self._IsActive = True
            for comp in self.Components.values():
                if isinstance(comp, GameScript):
                    comp.OnActivate()

    def Deactivate(self):
        if self._IsActive:
            self._IsActive = False
            for comp in self.Components.values():
                if isinstance(comp, GameScript):
                    comp.OnDeactivate()

    def AddComponent(self, component_class, *args, **kwargs):
        component_instance = component_class(*args, **kwargs)

        if isinstance(component_instance, GameScript):
            component_instance.Entity = self

        self.Components[component_class] = component_instance

        if self._IsActive and isinstance(component_instance, GameScript):
            component_instance.OnActivate()

        return component_instance

    def GetComponent(self, component_class):
        if component_class in self.Components:
            return self.Components[component_class]

        for cls, instance in self.Components.items():
            if issubclass(cls, component_class):
                return instance
        return None

    def HasComponent(self, component_class):
        if component_class in self.Components:
            return True
        return any(issubclass(cls, component_class) for cls in self.Components.keys())
