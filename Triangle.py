class Triangle:
    def __init__(self, v0, v1, v2, colour=(255, 255, 255)):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.colour = colour
    
    def normal(self):
        edge1 = self.v1.position - self.v0.position
        edge2 = self.v2.position - self.v0.position
        return edge1.cross(edge2).normalised
    
    def is_backface(self):
        return self.normal().dot(self.v0.position) >= 0