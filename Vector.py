class Vector4:
    def __init__(self, x=None, y=None, z=None, w=1):
        if isinstance(x, Vector4):
            # Copy constructor
            self.x, self.y, self.z, self.w = x.x, x.y, x.z, x.w
        elif isinstance(x, (list, tuple)) and len(x) == 4:
            # Initialize from list or tuple
            self.x, self.y, self.z, self.w = x
        elif all(v is not None for v in (x, y, z, w)):
            # Initialize from four separate values
            self.x, self.y, self.z, self.w = x, y, z, w
        else:
            raise ValueError(
                'Vector4 must be initialized with either another Vector4, '
                'a list/tuple of 4 floats, or four separate float values.'
            )
    
    def __repr__(self):
        return f'Vector4(x={self.x}, y={self.y}, z={self.z}, w={self.w})'

    def __eq__(self, other):
        if (self.x, self.y, self.z, self.w) == (other.x, other.y, other.z, other.w):
            return True
        return False
    
    def __add__(self, other):
        return Vector4(self.x+other.x, self.y+other.y, self.z+other.z, self.w)

    def __sub__(self, other):
        return Vector4(self.x-other.x, self.y-other.y, self.z-other.z, self.w)

    def __mul__(self, scalar):
        return Vector4(self.x*scalar, self.y*scalar, self.z*scalar, self.w)
    
    def __truediv__(self, scalar):
        return Vector4(self.x/scalar, self.y/scalar, self.z/scalar, self.w)
    
    def perspective_divide(self):
        if self.w != 0:
            return Vector4(self.x / self.w, self.y / self.w, self.z / self.w, 1)
        return self

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def cross(self, other):
        return Vector4(self.y*other.z - self.z*other.y,
                       self.z*other.x - self.x*other.z,
                       self.x*other.y - self.y*other.x,
                       self.w)

    @property
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    @property
    def normalised(self):
        return self*(1/self.length)

    def to_list(self):
        return [self.x, self.y, self.z, self.w]
    
    def to_vector3(self):
        return Vector3(self)


class Vector3:
    def __init__(self, x=None, y=None, z=None):
        if isinstance(x, Vector3) or isinstance(x, Vector4):
            # Copy constructor
            self.x, self.y, self.z = x.x, x.y, x.z
        elif isinstance(x, (list, tuple)) and len(x) == 4:
            # Initialize from list or tuple
            self.x, self.y, self.z = x
        elif all(v is not None for v in (x, y, z)):
            # Initialize from three separate values
            self.x, self.y, self.z = x, y, z
        else:
            raise ValueError(
                'Vector3 must be initialized with either another Vector4, '
                'a list/tuple of 3 floats, or three separate float values.'
            )
    
    def __repr__(self):
        return f'Vector3(x={self.x}, y={self.y}, z={self.z})'

    def __eq__(self, other):
        if (self.x, self.y, self.z) == (other.x, other.y, other.z):
            return True
        return False
    
    def __add__(self, other):
        return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)

    def __mul__(self, scalar):
        return Vector3(self.x*scalar, self.y*scalar, self.z*scalar)

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def cross(self, other):
        return Vector3(self.y*other.z - self.z*other.y,
                       self.z*other.x - self.x*other.z,
                       self.x*other.y - self.y*other.x)

    @property
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    @property
    def normalised(self):
        return self*(1/self.length)

    def to_list(self):
        return [self.x, self.y, self.z]
    
    def to_vector4(self, w):
        return Vector4(self.x, self.y, self.z, w)
