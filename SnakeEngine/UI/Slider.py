from .Extent import UIExtent


class UISlider:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        value=0.5,
        bg_color=(0.1, 0.1, 0.1, 1.0),
        fill_color=(0.0, 0.7, 0.0, 1.0),
    ):
        self.Bounds = UIExtent(x, y, width, height)
        self.Value = float(value)
        self.BackgroundColor = bg_color
        self.FillColor = fill_color
        self.IsDragging = False
