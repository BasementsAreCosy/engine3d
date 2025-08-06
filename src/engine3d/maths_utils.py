import numpy as np

def normalise(vec):
    norm = np.linalg.norm(vec[:3])
    if norm > 0:
        normalised_xyz = vec[:3] / norm
    else:
        normalised_xyz = vec[:3]
    
    return np.array([*normalised_xyz, vec[3]], dtype=np.float32)

def cross_product(a, b):
    cross_xyz = np.cross(a[:3], b[:3])
    
    w = a[3]
    
    return np.array([*cross_xyz, w], dtype=np.float32)
