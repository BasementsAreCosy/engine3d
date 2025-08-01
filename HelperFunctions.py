import numpy as np
import math

def normalise(vec):
    norm = np.linalg.norm(vec[:3])
    if norm > 0:
        normalised_xyz = vec[:3] / norm
    else:
        normalised_xyz = vec[:3]
    
    return np.array([*normalised_xyz, vec[3]], dtype=np.float32)

def cross_product(a, b):
    # Compute cross product of xyz parts
    cross_xyz = np.cross(a[:3], b[:3])
    
    # Extract w from a
    w = a[3]
    
    # Concatenate cross product xyz with original w
    return np.array([*cross_xyz, w], dtype=np.float32)

def is_backface(tri):
    return normalise(cross_product(tri[1]-tri[0], tri[2]-tri[0])).dot(tri[0]) >= 0

def is_backface_batch(tris):
    # Get the 3D components (ignore w)
    a = tris[:, 0, :3]
    b = tris[:, 1, :3]
    c = tris[:, 2, :3]

    ab = b - a
    ac = c - a

    # Cross product to get normal vector
    normals = np.cross(ab, ac)

    # Check if z component is >= 0 (facing away from camera)
    return normals[:, 2] >= 0

def identity():
    return np.identity(4, dtype=np.float32)

def translation(tx, ty, tz):
    mat = np.identity(4, dtype=np.float32)
    mat[0, 3] = tx
    mat[1, 3] = ty
    mat[2, 3] = tz
    return mat

def scaling(sx, sy, sz):
    mat = np.identity(4, dtype=np.float32)
    mat[0, 0] = sx
    mat[1, 1] = sy
    mat[2, 2] = sz
    return mat

def rotation_x(theta):
    mat = np.identity(4, dtype=np.float32)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    mat[1, 1] = cos_t
    mat[1, 2] = -sin_t
    mat[2, 1] = sin_t
    mat[2, 2] = cos_t
    return mat

def rotation_y(theta):
    mat = np.identity(4, dtype=np.float32)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    mat[0, 0] = cos_t
    mat[0, 2] = sin_t
    mat[2, 0] = -sin_t
    mat[2, 2] = cos_t
    return mat

def rotation_z(theta):
    mat = np.identity(4, dtype=np.float32)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    mat[0, 0] = cos_t
    mat[0, 1] = -sin_t
    mat[1, 0] = sin_t
    mat[1, 1] = cos_t
    return mat