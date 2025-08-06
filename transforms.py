import numpy as np
import math

def translation_matrix(tx, ty, tz):
    mat = np.identity(4, dtype=np.float32)
    mat[0, 3] = tx
    mat[1, 3] = ty
    mat[2, 3] = tz
    return mat

def scaling_matrix(sx, sy, sz):
    mat = np.identity(4, dtype=np.float32)
    mat[0, 0] = sx
    mat[1, 1] = sy
    mat[2, 2] = sz
    return mat

def rotation_matrix_x(theta):
    mat = np.identity(4, dtype=np.float32)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    mat[1, 1] = cos_t
    mat[1, 2] = -sin_t
    mat[2, 1] = sin_t
    mat[2, 2] = cos_t
    return mat

def rotation_matrix_y(theta):
    mat = np.identity(4, dtype=np.float32)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    mat[0, 0] = cos_t
    mat[0, 2] = sin_t
    mat[2, 0] = -sin_t
    mat[2, 2] = cos_t
    return mat

def rotation_matrix_z(theta):
    mat = np.identity(4, dtype=np.float32)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    mat[0, 0] = cos_t
    mat[0, 1] = -sin_t
    mat[1, 0] = sin_t
    mat[1, 1] = cos_t
    return mat

def combined_rotation(x_alpha, y_beta, z_gamma):
    return rotation_matrix_z(z_gamma) @ rotation_matrix_y(y_beta) @ rotation_matrix_x(x_alpha)