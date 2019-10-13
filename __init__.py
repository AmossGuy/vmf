from collections import namedtuple
from math import sqrt

def make_cuboid(x, y, z, width, depth, height, material="dev/dev_measuregeneric01b", facealign=False):
    corner, w_edge, d_edge, h_edge = Vector3(x, y, z), Vector3(width, 0, 0), Vector3(0, depth, 0), Vector3(0, 0, height)
    planes = [
        BrushFace(corner + d_edge + h_edge, corner + w_edge + d_edge + h_edge, corner + w_edge + h_edge, material, facealign),
        BrushFace(corner, corner + w_edge, corner + w_edge + d_edge, material, facealign),
        BrushFace(corner + d_edge + h_edge, corner + h_edge, corner, material, facealign),
        BrushFace(corner + w_edge + d_edge, corner + w_edge, corner + w_edge + h_edge, material, facealign),
        BrushFace(corner + w_edge + d_edge + h_edge, corner + d_edge + h_edge, corner + d_edge, material, facealign),
        BrushFace(corner + w_edge, corner, corner + h_edge, material, facealign)
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
        return type(self)(self.y * other.z - self.z * other.y,
                          self.z * other.x - self.x * other.z,
                          self.x * other.y - self.y * other.x)
    def length(self):
        return sqrt(self.dot(self))
    def normalize(self):
        return self / self.length()
    def angle(self, other):
        return acos(self.dot(other) / (self.length() * other.length()))
    def closestaxis(self):
        # Priority X > Y > Z
        t = abs(self)
        if t.x >= t.y >= t.z: return type(self)(1, 0, 0)
        if t.y >= t.z: return type(self)(0, 1, 0)
        return type(self)(0, 0, 1)

class UvAxis(namedtuple("UvAxis", ["normal", "offset", "scale"])):
    pass

def getnormalalign(normal):
    vector = Vector3(0, -1, 0) if normal.closestaxis() == Vector3(0, 0, 1) else Vector3(0, 0, -1) # This is basically asking whether this is a floor/ceiling or a wall
    uaxis = normal.cross(vector).normalize()
    vaxis = uaxis.cross(normal).normalize() # The Y axis of the texture is 90° away from the X axis
    return (UvAxis(uaxis, 0, 0.25), UvAxis(vaxis, 0, 0.25))

class BrushFace:
    def __init__(self, point1, point2, point3, material="dev/dev_measuregeneric01", facealign=False):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.material = material
        if not facealign:
            self.uaxis, self.vaxis = self.getworldalign()
        else:
            self.uaxis, self.vaxis = self.getfacealign()
    def getnormal(self):
        return (self.point1 - self.point2).cross(self.point3 - self.point2).normalize()
    def getworldalign(self):
        return getnormalalign(self.getnormal().closestaxis())
    def getfacealign(self):
        return getnormalalign(self.getnormal())

class Entity(namedtuple("Entity", ["classname", "origin", "keyvalues", "outputs", "solids"])):
    pass

class Output(namedtuple("Output", ["myoutput", "target", "theirinput", "parameter", "delay", "repeats"])):
    pass
