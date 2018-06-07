import math

from aecSpace.aecGeometry import aecGeometry

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return c

def create_mesh_side(vertices, normals, indices, index, height, a, b):
    c = [b[0], b[1], b[2] + height]
    d = [a[0], a[1], a[2] + height]
    vertices.extend(a)
    vertices.extend(b)
    vertices.extend(c)
    vertices.extend(d)
    indices.append(index)
    indices.append(index+1)
    indices.append(index+2)
    indices.append(index)
    indices.append(index+2)
    indices.append(index+3)
    index = index + 4
    v1l = math.sqrt(math.pow(b[0] - a[0], 2) + math.pow(b[1] - a[1], 2) + math.pow(b[2] - a[2], 2))
    v2l = math.sqrt(math.pow(c[0] - b[0], 2) + math.pow(c[1] - b[1], 2) + math.pow(c[2] - b[2], 2))
    v1 = [(b[0] - a[0])/v1l, (b[1] - a[1])/v1l, (b[2] - a[2])/v1l]
    v2 = [(c[0] - b[0])/v2l, (c[1] - b[1])/v2l, (c[2] - b[2])/v2l]
    n = cross(v1,v2)
    normals.extend(n)
    normals.extend(n)
    normals.extend(n)
    normals.extend(n)
    return index

def create_mesh_top_bottom(vertices, normals, indices, index, points, offset, normal):
    for point in points: 
        vertices.extend([point[0], point[1], point[2] + offset])
        normals.extend(normal)
        indices.append(index)
        
        index += 1
    return index

def glTFMesh(model, spaces, colorIndex):
    for space in spaces:
        index = 0
        points = [point.xyz for point in space.floor.points]
        points.reverse
        height = space.height
        vertices = []
        normals = []
        indices = []
        '''
        Create a mesh by using two edge points, and extrapolating 
        an upper edge by offseting the lower points by height.
        '''
        for i in range(0,len(points)):
            a = points[i]
            if i == len(points)-1:
                b = points[0]
            else:
                b = points[i+1]
            index = create_mesh_side(vertices, normals, indices, index, height, a, b)
        
        # Create the bottom      
        index = create_mesh_top_bottom(vertices, normals, indices, index, points[::-1], 0.0, [0.0,0.0,-1.0])
        
        # Create the top
        index = create_mesh_top_bottom(vertices, normals, indices, index, points, height, [0.0,0.0,1.0])

        # Write the mesh to glTF
        model.add_triangle_mesh(vertices, normals, indices, colorIndex)

    return model