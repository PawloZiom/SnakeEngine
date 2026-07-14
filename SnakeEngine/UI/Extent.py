from ..Core.Mathematics.Vector2 import Vector2


class UIExtent:
    def __init__(self, x, y, width, height):
        self.Position = Vector2(x, y)
        self.Width = float(width)
        self.Height = float(height)
