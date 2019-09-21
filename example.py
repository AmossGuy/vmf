import __init__ as vmf
from export import export_map

def generateexamplemap():
    size = vmf.Vector3(1024, 1024, 512)
    thickness = 16

    cubes = []
    for i in range(3):
        axis = [vmf.Vector3(1, 0, 0), vmf.Vector3(0, 1, 0), vmf.Vector3(0, 0, 1)][i]

        point = (-size/2)._replace(**{["x", "y", "z"][i]: size[i]/2})
        stuff = size._replace(**{["x", "y", "z"][i]: thickness})
        cubes.append(vmf.make_cube(*point, *stuff))

        point = (-size/2)._replace(**{["x", "y", "z"][i]: -size[i]/2-thickness})
        stuff = size._replace(**{["x", "y", "z"][i]: thickness})
        cubes.append(vmf.make_cube(*point, *stuff))

    return [vmf.Entity("worldspawn", vmf.Vector3(0, 0, 0), [["skyname", ""]], [], cubes), vmf.Entity("info_player_start", vmf.Vector3(0, 0, -size[2]/2), [], [], [])]

if __name__ == "__main__":
    print(export_map(generateexamplemap()))
