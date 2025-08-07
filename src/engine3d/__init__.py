# engine3d/__init__.py

from .engine import Window
from .primitives import cube_mesh, tetrahedron_mesh
from .Clock import Clock
# Add other top-level exports as needed

__all__ = ['Window', 'cube_mesh', 'tetrahedron_mesh', 'Clock']
