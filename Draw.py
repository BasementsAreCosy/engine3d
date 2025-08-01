import cv2
import numpy as np
import time
import logging

def to_screen_space(vertex, width=800, height=600):
    # Convert NDC (-1..1) to screen pixels (0..width-1, 0..height-1)
    x = int((vertex[0] + 1) * 0.5 * width)
    y = int((1 - (vertex[1] + 1) * 0.5) * height)  # Flip y axis
    return (x, y)

def draw_triangle_wireframe(window, tri, colour=(255, 0, 0)):
    pts = [to_screen_space(v, window.width, window.height) for v in [tri[0], tri[1], tri[2]]]
    
    cv2.line(window.backbuffer, pts[0], pts[1], colour, 1)
    cv2.line(window.backbuffer, pts[1], pts[2], colour, 1)
    cv2.line(window.backbuffer, pts[2], pts[0], colour, 1)

def draw_triangle_filled(window, tri, colour=(255, 255, 255)):
    pts = [to_screen_space(v, window.width, window.height) for v in [tri[0], tri[1], tri[2]]]
    
    tri_pts = np.array([
        pts[0],
        pts[1],
        pts[2]
    ], np.int32)

    cv2.fillConvexPoly(window.backbuffer, tri_pts, colour)

def is_inside_clip_space(v):
    x, y, z, w = v[0], v[1], v[2], v[3]
    return -w <= x <= w and -w <= y <= w and -w <= z <= w

def triangle_in_clip_space(triangle):
    return any(is_inside_clip_space(v) for v in [triangle[0], triangle[1], triangle[2]])

def triangle_in_clip_space_batch(tris):
    # w components, shape (N, 3, 1)
    w = tris[:, :, 3:4]

    # Broadcast to compare x/y/z to ±w
    xyz = tris[:, :, :3]

    in_bounds = np.logical_and(xyz >= -w, xyz <= w)  # shape: (N, 3, 3)

    # All coordinates of all 3 vertices must be within bounds
    return np.all(in_bounds, axis=(1, 2))

def render_mesh(window, mesh, camera): # Local -> Model -> View -> Projection (incl persp divide) -> Viewport Transform (to screen) Rasterisation -> Framebuffer (handled by window)
    start = time.perf_counter()
    view = camera.get_view_matrix()
    proj = camera.get_projection_matrix()
    end = time.perf_counter()
    logging.info(f'Get matrix: {end-start:.8f}')

    start = time.perf_counter()
    tris = mesh.get_transformed_triangles(view, proj)
    end = time.perf_counter()
    logging.info(f'Transform triangle: {end-start:.8f}')

    start = time.perf_counter()
    for tri in tris:
        draw_triangle_filled(window, tri[0])
        draw_triangle_wireframe(window, tri[0])
    end = time.perf_counter()
    logging.info(f'Draw: {end-start:.8f}')