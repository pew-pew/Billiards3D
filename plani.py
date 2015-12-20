class Sphere:
    def __init__(self, x, y, z, R):
        self.x = x
        self.y = y
        self.z = z 
        self.R = R
        
    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5 - self.R - other.R


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
   
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
   
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)
   
    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other, self.z + other)
   
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def lenSq(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2
   

def progection(self, other):
    if abs(other) == 0:
        return Vector(0, 0, 0)
    X = self.x
    Y = self.y
    Z = self.z
    Xpro = X * (other.x / abs(other))
    Ypro = Y * (other.y / abs(other))
    Zpro = Z * (other.z / abs(other))
    return (other * (1 / abs(other))) * (Xpro + Ypro + Zpro)

def bump(first, second, line):
    Fpro = progection(first, line)
    Spro = progection(second, line)
    return first + Fpro * (-1) + Spro, second + Spro * (-1) + Fpro