import math
import numpy as np

import maths_utils

class Camera:
    def __init__(self, aspect_ratio=None, position=None, target=None, up=None, fov=None, near=None, far=None):
        if aspect_ratio is None:
            aspect_ratio = 1
        if position is None:
            position = np.array([0, 0, 0, 1], dtype=np.float32)
        if target is None:
            target = np.array([0, 0, 0, 1], dtype=np.float32)
        if up is None:
            up = np.array([0, 1, 0, 0], dtype=np.float32)
        if fov is None:
            fov = 90
        if near is None:
            near = 0.1
        if far is None:
            far = 1000
        
        
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
    
    def get_view_matrix(self):
        forward = maths_utils.normalise(self.position - self.target)
        right = maths_utils.normalise(maths_utils.cross_product(self.up, forward))
        up = maths_utils.cross_product(forward, right)

        view = np.array([
            [right[0], right[1], right[2], -right.dot(self.position)],
            [up[0], up[1], up[2], -up.dot(self.position)],
            [forward[0], forward[1], forward[2], -forward.dot(self.position)],
            [0, 0, 0, 1]
        ])

        return view.T

    def get_projection_matrix(self):
        f = 1 / math.tan(math.radians(self.fov) / 2)
        
        return np.array([
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near) / (self.near - self.far), (2 * self.far * self.near) / (self.near - self.far)],
            [0, 0, -1, 0]
        ]).T