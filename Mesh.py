from Vertex import Vertex
from Triangle import Triangle
from Vector import Vector4
from Matrix4x4 import Matrix
from Draw import triangle_in_clip_space

class Mesh:
    def __init__(self, triangles, position=Vector4(0, 0, 0, 1), rotation=Vector4(0, 0, 0, 0), scale=Vector4(1, 1, 1, 0)):
        self.triangles = triangles
        self.position = position
        self.rotation = rotation
        self.scale = scale
    
    def apply_transform(self, matrix):
        new_triangles = []
        for triangle in self.triangles:
            v0 = Vertex(matrix.transform(triangle.v0.position), triangle.v0.normal, triangle.v0.uv)
            v1 = Vertex(matrix.transform(triangle.v1.position), triangle.v1.normal, triangle.v1.uv)
            v2 = Vertex(matrix.transform(triangle.v2.position), triangle.v2.normal, triangle.v2.uv)
            new_triangles.append(Triangle(v0, v1, v2, triangle.colour))
        return new_triangles

    def get_transformed_triangles(self, view_matrix, proj_matrix):
        model_matrix = self.get_model_matrix()
        transformed_tris = []

        for tri in self.triangles:
            # Transform each vertex position to world space
            v0_world = Vertex(model_matrix.transform(tri.v0.position))
            v1_world = Vertex(model_matrix.transform(tri.v1.position))
            v2_world = Vertex(model_matrix.transform(tri.v2.position))

            # Transform to view space (camera)
            v0_view = Vertex(view_matrix.transform(v0_world.position))
            v1_view = Vertex(view_matrix.transform(v1_world.position))
            v2_view = Vertex(view_matrix.transform(v2_world.position))

            # Check if facing camera
            if Triangle(v0_view, v1_view, v2_view).is_backface():
                continue

            # Project to 2D screen space
            v0_proj = Vertex(proj_matrix.transform(v0_view.position))
            v1_proj = Vertex(proj_matrix.transform(v1_view.position))
            v2_proj = Vertex(proj_matrix.transform(v2_view.position))

            # Perform perspective divide (if your transform method doesn't do it)
            v0_ndc = Vertex(v0_proj.position.perspective_divide())
            v1_ndc = Vertex(v1_proj.position.perspective_divide())
            v2_ndc = Vertex(v2_proj.position.perspective_divide())

            # Check if in clip space
            if not triangle_in_clip_space(Triangle(v0_ndc, v1_ndc, v2_ndc)):
                continue

            # Create new vertices (ignoring normals and uv for now)
            new_v0 = v0_ndc
            new_v1 = v1_ndc
            new_v2 = v2_ndc

            # Keep color if present
            color = getattr(tri, 'color', (255, 255, 255))

            transformed_tris.append(Triangle(new_v0, new_v1, new_v2, color))

        return transformed_tris
    
    def get_model_matrix(self):
        """
        Construct the model transformation matrix from the mesh's
        position, rotation (Euler angles in radians), and scale.
        """
        # Translation matrix
        t = Matrix.translation(self.position.x, self.position.y, self.position.z)
        
        # Rotation matrices for each axis
        rx = Matrix.rotation_x(self.rotation.x)
        ry = Matrix.rotation_y(self.rotation.y)
        rz = Matrix.rotation_z(self.rotation.z)
        
        # Combined rotation (order: Z * Y * X)
        r = rz * ry * rx
        
        # Scaling matrix
        s = Matrix.scaling(self.scale.x, self.scale.y, self.scale.z)
        
        # Model matrix = Translation * Rotation * Scale
        return t * r * s
    
    def rotate(self, x=0, y=0, z=0):
        self.rotation.x += x
        self.rotation.y += y
        self.rotation.z += z
    
    def set_rotation(self, x=0, y=0, z=0):
        if isinstance(x, Vector4):
            self.rotation = x
        else:
            self.rotation = Vector4(x, y, z, 0)

    @staticmethod
    def cube():
        verts = [
            # Front
            Vertex(Vector4(-1, -1,  1, 1)), Vertex(Vector4( 1, -1,  1, 1)), Vertex(Vector4( 1,  1,  1, 1)),
            Vertex(Vector4(-1,  1,  1, 1)),
            # Back
            Vertex(Vector4(-1, -1, -1, 1)), Vertex(Vector4( 1, -1, -1, 1)), Vertex(Vector4( 1,  1, -1, 1)),
            Vertex(Vector4(-1,  1, -1, 1)),
        ]

        idx = [
            (0, 1, 2), (0, 2, 3),  # Front
            (1, 5, 6), (1, 6, 2),  # Right
            (5, 4, 7), (5, 7, 6),  # Back
            (4, 0, 3), (4, 3, 7),  # Left
            (3, 2, 6), (3, 6, 7),  # Top
            (4, 5, 1), (4, 1, 0),  # Bottom
        ]

        tris = [Triangle(verts[i], verts[j], verts[k]) for i, j, k in idx]
        return Mesh(tris)
