from .GameEntity import GameEntity


class Scene:
    def __init__(self):
        self.Entities = []

    def CreateEntity(self):
        entity = GameEntity()
        self.Entities.append(entity)
        return entity
