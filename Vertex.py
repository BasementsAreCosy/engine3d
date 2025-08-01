class Vertex:
    def __init__(self, position, normal=None, uv=None):
        self.position = position
        self.normal = normal
        self.uv = uv
    
    def __repr__(self):
        return f'Vertex(position={self.position}, normal={self.normal}, uv={self.uv})'