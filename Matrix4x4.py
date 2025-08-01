from Vector import Vector4
import math

class Matrix:
    def __init__(self, data=None):
        '''
        Initialize the matrix.
        Accepts:
          - None: creates identity matrix
          - flat list of 16 floats
          - 2D list (4x4)
          - another Matrix4x4 instance
        '''
        if data is None:
            # Identity matrix
            self.data = self.identity()
        elif isinstance(data, Matrix):
            # Copy from another matrix
            self.data = [row[:] for row in data.data]
        elif isinstance(data, list):
            # Could be flat list or 2D list
            if len(data) == 16 and all(isinstance(x, (int, float)) for x in data):
                # flat list
                self.data = [
                    data[0:4],
                    data[4:8],
                    data[8:12],
                    data[12:16],
                ]
            elif (
                len(data) == 4
                and all(isinstance(row, list) and len(row) == 4 for row in data)
            ):
                # 2D list (4x4)
                self.data = [row[:] for row in data]
            else:
                raise ValueError(
                    'List must be a flat list of 16 floats or a 4x4 2D list.'
                )
        else:
            raise TypeError(
                'Matrix4x4 constructor accepts None, Matrix4x4 instance, or list.'
            )

    def __mul__(self, other):
        if isinstance(other, Matrix):
            # Matrix multiplication
            result_data = [[0]*4 for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    # Compute element (i,j)
                    total = 0
                    for k in range(4):
                        total += self.data[i][k] * other.data[k][j]
                    result_data[i][j] = total
            return Matrix(result_data)

        elif hasattr(other, 'x') and hasattr(other, 'y') and hasattr(other, 'z') and hasattr(other, 'w'):
            # Assume Vector4-like object
            x, y, z, w = other.x, other.y, other.z, other.w

            x_new = (self.data[0][0] * x +
                     self.data[0][1] * y +
                     self.data[0][2] * z +
                     self.data[0][3] * w)

            y_new = (self.data[1][0] * x +
                     self.data[1][1] * y +
                     self.data[1][2] * z +
                     self.data[1][3] * w)

            z_new = (self.data[2][0] * x +
                     self.data[2][1] * y +
                     self.data[2][2] * z +
                     self.data[2][3] * w)

            w_new = (self.data[3][0] * x +
                     self.data[3][1] * y +
                     self.data[3][2] * z +
                     self.data[3][3] * w)

            if w_new != 0:
                x_new /= w_new
                y_new /= w_new
                z_new /= w_new

            return Vector4(x_new, y_new, z_new, 1)

        else:
            raise TypeError(f'Unsupported multiplication with {type(other)}')
    
    @staticmethod
    def identity():
        return Matrix([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ])

    @staticmethod
    def translation(tx, ty, tz):
        return Matrix([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def scaling(sx, sy, sz):
        return Matrix([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_x(theta):
        return Matrix([
            [1, 0, 0, 0],
            [0, math.cos(theta), -math.sin(theta), 0],
            [0, math.sin(theta), math.cos(theta), 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_y(theta):
        return Matrix([
            [math.cos(theta), 0, math.sin(theta), 0],
            [0, 1, 0, 0],
            [-math.sin(theta), 0, math.cos(theta), 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(theta):
        return Matrix([
            [math.cos(theta), -math.sin(theta), 0, 0],
            [math.sin(theta), math.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def transform(self, vector):
        if hasattr(vector, 'x') and hasattr(vector, 'y') and hasattr(vector, 'z') and hasattr(vector, 'w'):
            x, y, z, w = vector.x, vector.y, vector.z, vector.w
        else:
            raise TypeError('Expected a vector with x, y, z, w attributes.')

        x_new = self.data[0][0] * x + self.data[0][1] * y + self.data[0][2] * z + self.data[0][3] * w
        y_new = self.data[1][0] * x + self.data[1][1] * y + self.data[1][2] * z + self.data[1][3] * w
        z_new = self.data[2][0] * x + self.data[2][1] * y + self.data[2][2] * z + self.data[2][3] * w
        w_new = self.data[3][0] * x + self.data[3][1] * y + self.data[3][2] * z + self.data[3][3] * w

        return Vector4(x_new, y_new, z_new, w_new)