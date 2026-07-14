import math


class Vector2:
    def __init__(self, X=0.0, Y=0.0):
        self.X = float(X)
        self.Y = float(Y)

    def __repr__(self):
        return f"Vector2({self.X}, {self.Y})"

    def __str__(self):
        return f"({self.X}, {self.Y})"

    def _to_vec(self, other):
        if isinstance(other, (int, float)):
            return Vector2(other, other)
        return other

    def Copy(self):
        return Vector2(self.X, self.Y)

    def __add__(self, other):
        other = self._to_vec(other)
        return Vector2(self.X + other.X, self.Y + other.Y)

    def __sub__(self, other):
        other = self._to_vec(other)
        return Vector2(self.X - other.X, self.Y - other.Y)

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector2(self.X * value, self.Y * value)

        value = self._to_vec(value)
        return Vector2(self.X * value.X, self.Y * value.Y)

    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            return Vector2(self.X / value, self.Y / value)
        raise TypeError("Vector2 division only supports scalar")

    def __iadd__(self, other):
        other = self._to_vec(other)
        self.X += other.X
        self.Y += other.Y
        return self

    def __isub__(self, other):
        other = self._to_vec(other)
        self.X -= other.X
        self.Y -= other.Y
        return self

    def __rmul__(self, value):
        return self.__mul__(value)

    def Length(self):
        return math.sqrt(self.X**2 + self.Y**2)

    def Normalize(self):
        length = self.Length()
        if length == 0:
            return Vector2(0, 0)
        return self / length

    def Dot(self, other):
        return self.X * other.X + self.Y * other.Y

    @staticmethod
    def Zero():
        return Vector2(0, 0)

    @staticmethod
    def One():
        return Vector2(1, 1)
