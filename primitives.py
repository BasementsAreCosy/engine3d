import numpy as np

def cube_mesh():
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
    return np.array(tris, dtype=np.float32)
