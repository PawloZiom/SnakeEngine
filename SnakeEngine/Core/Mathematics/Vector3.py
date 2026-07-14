import math


class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.X = float(x)
        self.Y = float(y)
        self.Z = float(z)

    def __repr__(self):
        return f"Vector3({self.X}, {self.Y}, {self.Z})"

    def __str__(self):
        return f"({self.X}, {self.Y}, {self.Z})"

    def _to_vec(self, other):
        if isinstance(other, (int, float)):
            return Vector3(other, other, other)
        return other

    def Copy(self):
        return Vector3(self.X, self.Y, self.Z)

    def __add__(self, other):
        other = self._to_vec(other)
        return Vector3(self.X + other.X, self.Y + other.Y, self.Z + other.Z)

    def __sub__(self, other):
        other = self._to_vec(other)
        return Vector3(self.X - other.X, self.Y - other.Y, self.Z - other.Z)

    def __iadd__(self, other):
        other = self._to_vec(other)
        self.X += other.X
        self.Y += other.Y
        self.Z += other.Z
        return self

    def __isub__(self, other):
        other = self._to_vec(other)
        self.X -= other.X
        self.Y -= other.Y
        self.Z -= other.Z
        return self

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector3(self.X * value, self.Y * value, self.Z * value)

        value = self._to_vec(value)
        return Vector3(self.X * value.X, self.Y * value.Y, self.Z * value.Z)

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            return Vector3(self.X / value, self.Y / value, self.Z / value)
        raise TypeError("Vector3 division only supports scalar")

    def Length(self):
        return math.sqrt(self.X**2 + self.Y**2 + self.Z**2)

    def Normalize(self):
        length = self.Length()
        if length == 0:
            return Vector3(0, 0, 0)
        return self / length

    def Dot(self, other):
        return self.X * other.X + self.Y * other.Y + self.Z * other.Z

    def Cross(self, other):
        other = self._to_vec(other)
        return Vector3(
            self.Y * other.Z - self.Z * other.Y,
            self.Z * other.X - self.X * other.Z,
            self.X * other.Y - self.Y * other.X,
        )

    @staticmethod
    def Zero():
        return Vector3(0, 0, 0)

    @staticmethod
    def One():
        return Vector3(1, 1, 1)
