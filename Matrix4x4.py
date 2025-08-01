import numpy as np
from Vector4 import Vector4
import math

class Matrix:
    def __init__(self, data=None):
        if data is None:
            self.data = np.identity(4, dtype=np.float32)
        elif isinstance(data, Matrix):
            self.data = np.array(data.data, dtype=np.float32)
        elif isinstance(data, np.ndarray):
            if data.shape == (4, 4):
                self.data = data.astype(np.float32)
            elif data.size == 16:
                self.data = data.reshape((4, 4)).astype(np.float32)
            else:
                raise ValueError("Numpy array must be shape (4,4) or size 16.")
        elif isinstance(data, list):
            arr = np.array(data, dtype=np.float32)
            if arr.shape == (4, 4):
                self.data = arr
            elif arr.size == 16:
                self.data = arr.reshape((4, 4))
            else:
                raise ValueError("List must be a flat list of 16 floats or a 4x4 list.")
        else:
            raise TypeError("Matrix constructor accepts None, another Matrix, numpy.ndarray, or a list.")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(np.dot(self.data, other.data))

        elif hasattr(other, 'x') and hasattr(other, 'y') and hasattr(other, 'z') and hasattr(other, 'w'):
            vec = np.array([other.x, other.y, other.z, other.w], dtype=np.float32)
            result = np.dot(self.data, vec)
            if result[3] != 0:
                result[0:3] /= result[3]
                result[3] = 1
            return Vector4(*result)

        else:
            raise TypeError(f"Unsupported multiplication with {type(other)}")

    def transform(self, vector):
        if hasattr(vector, 'x') and hasattr(vector, 'y') and hasattr(vector, 'z') and hasattr(vector, 'w'):
            vec = np.array([vector.x, vector.y, vector.z, vector.w], dtype=np.float32)
            result = np.dot(self.data, vec)
            return Vector4(*result)
        else:
            raise TypeError("Expected a vector with x, y, z, w attributes.")

    @staticmethod
    def identity():
        return Matrix(np.identity(4, dtype=np.float32))

    @staticmethod
    def translation(tx, ty, tz):
        mat = np.identity(4, dtype=np.float32)
        mat[0, 3] = tx
        mat[1, 3] = ty
        mat[2, 3] = tz
        return Matrix(mat)

    @staticmethod
    def scaling(sx, sy, sz):
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = sx
        mat[1, 1] = sy
        mat[2, 2] = sz
        return Matrix(mat)

    @staticmethod
    def rotation_x(theta):
        mat = np.identity(4, dtype=np.float32)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        mat[1, 1] = cos_t
        mat[1, 2] = -sin_t
        mat[2, 1] = sin_t
        mat[2, 2] = cos_t
        return Matrix(mat)

    @staticmethod
    def rotation_y(theta):
        mat = np.identity(4, dtype=np.float32)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        mat[0, 0] = cos_t
        mat[0, 2] = sin_t
        mat[2, 0] = -sin_t
        mat[2, 2] = cos_t
        return Matrix(mat)

    @staticmethod
    def rotation_z(theta):
        mat = np.identity(4, dtype=np.float32)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        mat[0, 0] = cos_t
        mat[0, 1] = -sin_t
        mat[1, 0] = sin_t
        mat[1, 1] = cos_t
        return Matrix(mat)