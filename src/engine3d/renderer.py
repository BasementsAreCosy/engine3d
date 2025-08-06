import cv2
import numpy as np


def render(window, tris: np.ndarray):
    view_matrix = window.camera.get_view_matrix()
    proj_matrix = window.camera.get_projection_matrix()
    transformed_tris = transform_triangles(tris, view_matrix, proj_matrix, window.width, window.height)
    cv2.fillPoly(window.backbuffer, transformed_tris, color=(255, 255, 255))
    cv2.polylines(window.backbuffer, transformed_tris, isClosed=True, color=(255, 0, 0))

def transform_triangles(tris: np.ndarray, view_matrix: np.ndarray, projection_matrix: np.ndarray, width, height) -> np.ndarray:
    vertices = tris.reshape(-1, 4).astype(np.float32)

    vertices_view = vertices @ view_matrix
    vertices_proj = vertices_view @ projection_matrix

    w = vertices_proj[:, 3:4]
    w_nonzero = w != 0
    vertices_ndc = np.empty_like(vertices_proj)
    vertices_ndc[w_nonzero[:, 0]] = vertices_proj[w_nonzero[:, 0]] / w[w_nonzero].reshape(-1, 1)
    vertices_ndc[~w_nonzero[:, 0]] = vertices_proj[~w_nonzero[:, 0]]

    num_tris = len(tris)
    verts = vertices_ndc.reshape((num_tris, 3, 4))

    mask_backface = is_backface(verts)
    mask_clip = in_clip_space(verts)

    visible_mask = mask_backface & mask_clip

    visible_verts = verts[visible_mask]
    #colours = np.full((len(visible_verts), 3), 255, dtype=np.uint8)

    screen_verts = to_screen_space(visible_verts, width, height)

    return screen_verts

def to_screen_space(tris, width=500, height=500):
    x = ((tris[..., 0] + 1) * 0.5 * width).astype(np.int32)
    y = ((1 - (tris[..., 1] + 1) * 0.5) * height).astype(np.int32)
    return np.stack((x, y), axis=-1)

def is_backface(tris: np.ndarray) -> np.ndarray:
    a = tris[:, 0, :3]
    b = tris[:, 1, :3]
    c = tris[:, 2, :3]

    ab = b - a
    ac = c - a

    normals = np.cross(ab, ac)

    return normals[:, 2] >= 0

def in_clip_space(tris: np.ndarray) -> np.ndarray:
    w = tris[:, :, 3:4]

    xyz = tris[:, :, :3]

    in_bounds = np.logical_and(xyz >= -w, xyz <= w)

    return np.any(np.all(in_bounds, axis=2), axis=(1))
