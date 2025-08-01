#from Matrix4x4 import Matrix
import numpy as np
from Draw import triangle_in_clip_space_batch
import time
import logging
from HelperFunctions import *

class Mesh:
    def __init__(self, triangles, position=np.array([0, 0, 0, 1], dtype=np.float32), rotation=np.array([0, 0, 0, 0], dtype=np.float32), scale=np.array([1, 1, 1, 0], dtype=np.float32)):
        self.triangles = triangles
        self.position = position
        self.rotation = rotation
        self.scale = scale
    
    def apply_transform(self, matrix):
        new_triangles = []
        for triangle in self.triangles:
            v0 = np.array([*matrix.transform(triangle.v0)], dtype=np.float32)
            v1 = np.array([*matrix.transform(triangle.v1)], dtype=np.float32)
            v2 = np.array([*matrix.transform(triangle.v2)], dtype=np.float32)
            new_triangles.append((np.array([v0, v1, v2]), np.array([255, 255, 255])))
        return new_triangles

    def get_transformed_triangles(self, view_matrix, proj_matrix):
        model_matrix = self.get_model_matrix()

        verticies = []
        for tri in self.triangles:
            verticies.extend([
                tri[0],
                tri[1],
                tri[2]
            ])
        verticies = np.array(verticies, dtype=np.float32)

        vertices_world = verticies @ model_matrix
        vertices_view = vertices_world @ view_matrix
        vertices_proj = vertices_view @ proj_matrix

        w = vertices_proj[:, 3:4]
        w_nonzero = w != 0
        vertices_ndc = np.empty_like(vertices_proj)
        vertices_ndc[w_nonzero[:, 0]] = vertices_proj[w_nonzero[:, 0]] / w[w_nonzero].reshape(-1, 1)
        vertices_ndc[~w_nonzero[:, 0]] = vertices_proj[~w_nonzero[:, 0]]

        num_tris = len(self.triangles)
        verts = vertices_ndc.reshape((num_tris, 3, 4))

        mask_backface = is_backface_batch(verts)
        mask_clip = triangle_in_clip_space_batch(verts)

        visible_mask = mask_backface & mask_clip

        visible_verts = verts[visible_mask]
        colours = np.full((len(visible_verts), 3), 255, dtype=np.uint8)
        transformed_tris = list(zip(visible_verts, colours))


        return transformed_tris
    
    def get_model_matrix(self):
        """
        Construct the model transformation matrix from the mesh's
        position, rotation (Euler angles in radians), and scale.
        """
        # Translation matrix
        t = translation(self.position[0], self.position[1], self.position[2])
        
        # Rotation matrices for each axis
        rx = rotation_x(self.rotation[0])
        ry = rotation_y(self.rotation[1])
        rz = rotation_z(self.rotation[2])
        
        # Combined rotation (order: Z * Y * X)
        r = rz @ ry @ rx
        
        # Scaling matrix
        s = scaling(self.scale[0], self.scale[1], self.scale[2])
        
        # Model matrix = Translation * Rotation * Scale
        return t @ r @ s
    
    def rotate(self, x=0, y=0, z=0):
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z
    
    def set_rotation(self, x=0, y=0, z=0):
        if isinstance(x, np.array):
            self.rotation = x
        else:
            self.rotation = np.array([x, y, z, 0], dtype=np.float32)

    @staticmethod
    def cube():
        verts = np.array([
            [-1, -1,  1, 1],  # Front face vertices
            [ 1, -1,  1, 1],
            [ 1,  1,  1, 1],
            [-1,  1,  1, 1],
            [-1, -1, -1, 1],  # Back face vertices
            [ 1, -1, -1, 1],
            [ 1,  1, -1, 1],
            [-1,  1, -1, 1],
        ], dtype=np.float32)

        idx = [
            (0, 1, 2), (0, 2, 3),  # Front
            (1, 5, 6), (1, 6, 2),  # Right
            (5, 4, 7), (5, 7, 6),  # Back
            (4, 0, 3), (4, 3, 7),  # Left
            (3, 2, 6), (3, 6, 7),  # Top
            (4, 5, 1), (4, 1, 0),  # Bottom
        ]

        tris = [np.array([verts[i], verts[j], verts[k]]) for i, j, k in idx]
        return Mesh(tris)
