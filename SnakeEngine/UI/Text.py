from ..Core.Mathematics.Vector2 import Vector2


class UIText:
    def __init__(self, text: str, x, y, scale=1.0, color=(0.0, 1.0, 0.0, 1.0)):
        self.Text = text
        self.Position = Vector2(x, y)
        self.Scale = float(scale)
        self.Color = color
