from .Text import UIText


class UILabel(UIText):
    def __init__(self, text: str, x, y, scale=1.0, color=(1.0, 1.0, 1.0, 1.0)):
        super().__init__(text, x, y, scale, color)
