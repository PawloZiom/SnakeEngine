from .Extent import UIExtent


class UIButton:
    def __init__(
        self,
        text: str,
        x,
        y,
        width,
        height,
        bg_color=(0.3, 0.3, 0.4, 1.0),
        text_color=(1.0, 1.0, 1.0, 1.0),
        callback=None,
    ):
        self.Bounds = UIExtent(x, y, width, height)
        self.Text = text
        self.BackgroundColor = bg_color
        self.TextColor = text_color
        self.Callback = callback
        self.IsHovered = False
