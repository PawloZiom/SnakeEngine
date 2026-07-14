from .Extent import UIExtent


class UIFrame:
    def __init__(self, x, y, width, height, color=(0.2, 0.2, 0.2, 0.8)):
        self.Bounds = UIExtent(x, y, width, height)
        self.Color = color
