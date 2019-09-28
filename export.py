class VmfClass:
    def __init__(self, name, properties=[], classes=[]):
        self.name, self.properties, self.classes = name, properties, classes

def export_string(string):
    return "\"{}\"".format(string)
def export_vmfclass(vmfclass):
    l = [vmfclass.name, "\n{\n"]
    for property in vmfclass.properties:
        l.append("{} {}\n".format(export_string(property[0]), export_string(property[1])))
    for subclass in vmfclass.classes:
        l.append(export_vmfclass(subclass))
    l.append("}\n")
    return "".join(l)

def export_map(entities):
    return "".join([export_vmfclass(export_entity(entity)) for entity in entities])
def export_entity(entity):
    return VmfClass("world" if entity.classname == "worldspawn" else "entity", [
        ["classname", entity.classname],
        ["origin", export_vector3(entity.origin)],
    ] + entity.keyvalues, [VmfClass("connections", entity.outputs)] + [export_solid(solid) for solid in entity.solids])
def export_solid(solid):
    return VmfClass("solid", [], [export_side(side) for side in solid])
def export_side(brushface):
    return VmfClass("side", [
        ["plane", "({}) ({}) ({})".format(export_vector3(brushface.point1),
                                   export_vector3(brushface.point2),
                                   export_vector3(brushface.point3))],
        ["material", brushface.material],
        ["uaxis", export_uvaxis(brushface.uaxis)],
        ["vaxis", export_uvaxis(brushface.vaxis)]
    ])
def export_vector3(vector3):
    return "{} {} {}".format(vector3.x, vector3.y, vector3.z)
def export_uvaxis(uvaxis):
    return "[{} {} {} {}] {}".format(uvaxis.normal.x, uvaxis.normal.y, uvaxis.normal.z, uvaxis.offset, uvaxis.scale)
def export_output(output):
    return [output.myoutput, "{},{},{},{},{}".format(output.target, output.theirinput, output.parameter, output.delay, output.repeats)]
