import numpy as np

class Vector4:
    def __init__(self, x=None, y=None, z=None, w=1):
        if isinstance(x, Vector4):
            self.data = np.copy(x.data)
        elif isinstance(x, (list, tuple, np.ndarray)) and len(x) == 4:
            self.data = np.array(x, dtype=np.float32)
        elif isinstance(x, (list, tuple, np.ndarray)) and len(x) == 3:
            self.data = np.array([x[0], x[1], x[2], 1], dtype=np.float32)
        elif all(v is not None for v in (x, y, z, w)):
            self.data = np.array([x, y, z, w], dtype=np.float32)
        else:
            raise ValueError("Vector4 must be initialized with another Vector4, a list/tuple of 4 values, or four separate values.")

    def __repr__(self):
        return f"Vector4(x={self.x}, y={self.y}, z={self.z}, w={self.w})"

    def __eq__(self, other):
        return np.allclose(self.data, other.data)

    def __add__(self, other):
        return Vector4(self.data[:3] + other.data[:3], self.w)

    def __sub__(self, other):
        return Vector4(self.data[:3] - other.data[:3], self.w)

    def __mul__(self, scalar):
        return Vector4(self.data[:3] * scalar, self.w)

    def __truediv__(self, scalar):
        return Vector4(self.data[:3] / scalar, self.w)

    def dot(self, other):
        return np.dot(self.data[:3], other.data[:3])

    def cross(self, other):
        return Vector4(np.cross(self.data[:3], other.data[:3]), self.w)

    def perspective_divide(self):
        if self.w != 0:
            divided = self.data[:3] / self.w
            return Vector4(*divided, 1)
        return Vector4(*self.data)

    @property
    def x(self): return self.data[0]
    @property
    def y(self): return self.data[1]
    @property
    def z(self): return self.data[2]
    @property
    def w(self): return self.data[3]

    @x.setter
    def x(self, value): self.data[0] = value
    @y.setter
    def y(self, value): self.data[1] = value
    @z.setter
    def z(self, value): self.data[2] = value
    @w.setter
    def w(self, value): self.data[3] = value

    @property
    def length(self):
        return np.linalg.norm(self.data[:3])

    @property
    def normalised(self):
        norm = self.length
        if norm == 0:
            return Vector4(0, 0, 0, self.w)
        return Vector4(self.data[:3] / norm, self.w)

    def to_list(self):
        return self.data.tolist()