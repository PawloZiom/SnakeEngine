class AudioSource:

    def __init__(self, entity):
        self.entity = entity
        self.Clip = None
        self.Loop = False
        self.Volume = 1.0
        self.Pitch = 1.0
        self.PlayOnAwake = False
        self.IsSpatial3D = True

    def Play(self):
        if self.Clip:
            pass

    def Stop(self):
        pass
