from Matrix4x4 import Matrix
from Vector import Vector4
import math

class Camera:
    def __init__(self, aspect_ratio=None, position=Vector4(0, 0, 0, 1), target=Vector4(0, 0, 0, 1), up=Vector4(0, 1, 0, 0), fov=90, near=0.1, far=10000):
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
    
    def get_view_matrix(self):
        forward = (self.position - self.target).normalised
        right = self.up.cross(forward).normalised
        up = forward.cross(right)

        view = Matrix([
            [right.x, right.y, right.z, -right.dot(self.position)],
            [up.x, up.y, up.z, -up.dot(self.position)],
            [forward.x, forward.y, forward.z, -forward.dot(self.position)],
            [0, 0, 0, 1]
        ])

        return view

    def get_projection_matrix(self):
        f = 1 / math.tan(math.radians(self.fov) / 2)
        
        return Matrix([
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near) / (self.near - self.far), (2 * self.far * self.near) / (self.near - self.far)],
            [0, 0, -1, 0]
        ])