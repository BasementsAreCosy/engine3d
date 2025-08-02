#from Matrix4x4 import Matrix
import math
import numpy as np
from HelperFunctions import *

class Camera:
    def __init__(self, aspect_ratio=None, position=vector4(0, 0, 0, 1), target=vector4(0, 0, 0, 1), up=vector4(0, 1, 0, 0), fov=90, near=0.1, far=10000):
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
    
    def get_view_matrix(self):
        forward = normalise(self.position - self.target)
        right = normalise(cross_product(self.up, forward))
        up = cross_product(forward, right)

        view = np.array([
            [right[0], right[1], right[2], -right.dot(self.position)],
            [up[0], up[1], up[2], -up.dot(self.position)],
            [forward[0], forward[1], forward[2], -forward.dot(self.position)],
            [0, 0, 0, 1]
        ])

        return view

    def get_projection_matrix(self):
        f = 1 / math.tan(math.radians(self.fov) / 2)
        
        return np.array([
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near) / (self.near - self.far), (2 * self.far * self.near) / (self.near - self.far)],
            [0, 0, -1, 0]
        ])