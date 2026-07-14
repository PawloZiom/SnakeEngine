class AudioClip:

    def __init__(self, filepath: str):
        self.Filepath = filepath
        self.Duration = 0.0
        self.Loaded = False
