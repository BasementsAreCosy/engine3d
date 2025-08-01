import cv2
import numpy as np


def to_screen_space(vertex, width=800, height=600):
    # Convert NDC (-1..1) to screen pixels (0..width-1, 0..height-1)
    x = int((vertex.position.x + 1) * 0.5 * width)
    y = int((1 - (vertex.position.y + 1) * 0.5) * height)  # Flip y axis
    return (x, y)

def draw_triangle_wireframe(window, tri, colour=(255, 0, 0)):
    pts = [to_screen_space(v, window.width, window.height) for v in [tri.v0, tri.v1, tri.v2]]
    
    cv2.line(window.backbuffer, pts[0], pts[1], colour, 1)
    cv2.line(window.backbuffer, pts[1], pts[2], colour, 1)
    cv2.line(window.backbuffer, pts[2], pts[0], colour, 1)

def draw_triangle_filled(window, tri, colour=(255, 255, 255)):
    pts = [to_screen_space(v, window.width, window.height) for v in [tri.v0, tri.v1, tri.v2]]
    
    tri_pts = np.array([
        pts[0],
        pts[1],
        pts[2]
    ], np.int32)

    cv2.fillConvexPoly(window.backbuffer, tri_pts, colour)

def is_inside_clip_space(v):
    x, y, z, w = v.x, v.y, v.z, v.w
    return -w <= x <= w and -w <= y <= w and -w <= z <= w

def triangle_in_clip_space(triangle):
    return any(is_inside_clip_space(v.position) for v in [triangle.v0, triangle.v1, triangle.v2])

def render_mesh(window, mesh, camera): # Local -> Model -> View -> Projection (incl persp divide) -> Viewport Transform (to screen) Rasterisation -> Framebuffer (handled by window)
    view = camera.get_view_matrix()
    proj = camera.get_projection_matrix()

    tris = mesh.get_transformed_triangles(view, proj)
    
    for tri in tris:
        draw_triangle_filled(window, tri)
        draw_triangle_wireframe(window, tri)
    