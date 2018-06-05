import random

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer

from hypar import glTF

siteBoundary = \
{
     "type": "Polygon",
     "coordinates": \
     [
        [2000.1994, 2289.2733],
        [2700.4829, 2289.2733],
        [2700.4829, 1737.8546],
        [2108.5229, 1263.0727],
        [1792.2478, 1263.0727],
        [1771.8803, 1282.6400]          
     ]
}

buildings = \
[
    {
        'area' : 180000,
        'color' : aecColor.blue,
        'diameter' : (150, 200),
        'height' : 40,
        'level' : 0,
        'name' : 'Headquarters',
    }
]

def sitePlacement():
    spacer = aecSpacer()        
    site = aecSpace()
    sitePoints = [aecPoint(coord[0], coord[1]) for coord in siteBoundary["coordinates"]]
    site.boundary = sitePoints
    site.color = aecColor.green
    site.height = -0.1
    spaces = []
    xWidth = buildings[0]['diameter'][random.randint(0, 1)]
    yDepth = xWidth * 1.618
    building = aecSpace()
    building.makeBox(aecPoint(0, 0, 0), xDist = xWidth, yDist = yDepth)
    building.rotate(random.randint(0, 360))
    if spacer.placeWithin(building, site):
        building.height = buildings[0]['height']
        building.level = buildings[0]['level']
        building.color = buildings[0]['color']
        spaces += [building]
        spaces += spacer.stackToArea(building, buildings[0]['area'])
    area = 0
    floors = 0
    for space in spaces:
        area += space.area
        floors += 1
    spaces += [site]
        
    # Create a model to hold the geometry.
    model = glTF()

    # Create a material to use in the model.
    model.add_material(0.0, 0.0, 1.0, 0.9, 1.0, "Blue")
    model.add_material(0.0, 1.0, 0.0, 0.9, 1.0, "Green")

    for space in spaces:
        spaceMesh = space.mesh_graphic
        model.add_triangle_mesh(spaceMesh['vertices'], spaceMesh['normals'], spaceMesh['indices'], 0)
    
    return {"model": model.save_base64(), 'computed':{'floors':floors, 'area':area}}




