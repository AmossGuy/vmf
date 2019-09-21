from collections import namedtuple
from math import sqrt

def make_cube(x, y, z, width, depth, height, material="dev/dev_measuregeneric01"):
    corner, w_edge, d_edge, h_edge = Vector3(x, y, z), Vector3(width, 0, 0), Vector3(0, depth, 0), Vector3(0, 0, height)
    planes = [
        BrushFace(corner + d_edge + h_edge, corner + w_edge + d_edge + h_edge, corner + w_edge + h_edge, material),
        BrushFace(corner, corner + w_edge, corner + w_edge + d_edge, material),
        BrushFace(corner + d_edge + h_edge, corner + h_edge, corner, material),
        BrushFace(corner + w_edge + d_edge, corner + w_edge, corner + w_edge + h_edge, material),
        BrushFace(corner + w_edge + d_edge + h_edge, corner + d_edge + h_edge, corner + d_edge, material),
        BrushFace(corner + w_edge, corner, corner + h_edge, material)
    ]
    return planes

class Vector3(namedtuple("Vector3", ["x", "y", "z"])):
    def __abs__(self):
        return type(self)(*[abs(s) for s in self])
    def __add__(self, other):
        return type(self)(*[s + o for s, o in zip(self, other)])
    def __sub__(self, other):
        return type(self)(*[s - o for s, o in zip(self, other)])
    def __neg__ (self):
        return type(self)(*[-s for s in self])
    def __mul__(self, other):
        return type(self)(*[s * other for s in self])
    def __truediv__(self, other):
        return type(self)(*[s / other for s in self])
    def dot(self, other):
        return sum([s * o for s, o in zip(self, other)])
    def cross(self, other):
        return type(self)(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    def length(self):
        return sqrt(self.dot(self))
    def normalize(self):
        return self / self.length()
    def angle(self, other):
        return acos(self.dot(other) / (self.length() * other.length()))
    def closestaxis(self):
        # Priority X > Y > Z
        t = abs(self)
        if t.x >= t.y and t.x >= t.z: return type(self)(1, 0, 0)
        if t.y >= t.z: return type(self)(0, 1, 0)
        return type(self)(0, 0, 1)

class UvAxis(namedtuple("UvAxis", ["normal", "offset", "scale"])):
    pass

class BrushFace:
    def __init__(self, point1, point2, point3, material="dev/dev_measuregeneric01"):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.material = material
        self.uaxis, self.vaxis = self.getworldalign()
    def getnormal(self):
        return (self.point1 - self.point2).cross(self.point3 - self.point2).normalize()
    def getworldalign(self):
        vector = Vector3(0, -1, 0) if self.getnormal().closestaxis() == Vector3(0, 0, 1) else Vector3(0, 0, -1) # This is basically asking whether this is a floor/ceiling or a wall
        uaxis = self.getnormal().closestaxis().cross(vector).normalize()
        vaxis = uaxis.cross(self.getnormal()).normalize() # The Y axis of the texture is 90° away from the X axis
        return (UvAxis(uaxis, 0, 0.25), UvAxis(vaxis, 0, 0.25))
    def getfacealign(self):
        vector = Vector3(0, -1, 0) if self.getnormal().closestaxis() == Vector3(0, 0, 1) else Vector3(0, 0, -1) # This is basically asking whether this is a floor/ceiling or a wall
        uaxis = self.getnormal().cross(vector).normalize()
        vaxis = uaxis.cross(self.getnormal()).normalize() # The Y axis of the texture is 90° away from the X axis
        return (UvAxis(uaxis, 0, 0.25), UvAxis(vaxis, 0, 0.25))

class Entity(namedtuple("Entity", ["classname", "origin", "keyvalues", "outputs", "solids"])):
    pass

class Output(namedtuple("Output", ["myoutput", "target", "theirinput", "parameter", "delay", "repeats"])):
    pass

if __name__ == "__main__":
    p1, p2, p3 = Vector3(-55.4256, -32, 90.5097), Vector3(55.4256, 32, 90.5097), Vector3(100.68, -46.3837, 0)
    face = BrushFace(p1, p2, p3)
    print(face.uaxis, face.vaxis)