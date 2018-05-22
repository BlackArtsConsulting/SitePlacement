import random

from .aecColors import aecColors
from .aecSpace import aecSpace
from .aecSpacer import aecSpacer

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
        'color' : aecColors.blue,
        'diameter' : (150, 200),
        'height' : 40,
        'level' : 0,
        'name' : 'Headquarters',
    }
]

def sitePlacement():
    spacer = aecSpacer()        
    site = aecSpace()
    sitePoints = siteBoundary["coordinates"]
    site.setBoundary(sitePoints)
    site.setColor(aecColors.green)
    site.setHeight(-0.1)
    spaces = []
    building = buildings[0]
    xWidth = building['diameter'][random.randint(0, 1)]
    yDepth = xWidth * 1.618
    space = aecSpace()
    space.makeCross((0, 0, 0), (xWidth, yDepth, 0))
    space.rotate(random.randint(0, 360))
    if spacer.placeWithin(space, site):
        space.setHeight(building['height'])
        space.setLevel(building['level'])
        space.setColor(building['color'])
        spaces += [space]
        space2 = spacer.stackToArea(space, building['area'])
        spaces += space2
    area = 0
    floors = 0
    for space in spaces:
        area += space.getArea()
        floors += 1
    spaces += [site]
        
    # Create a model to hold the geometry.
    model = glTF()

    # Create a material to use in the model.
    model.add_material(0.0, 0.0, 1.0, 0.9, 1.0, "Blue")
    model.add_material(0.0, 1.0, 0.0, 0.9, 1.0, "Green")

    for space in spaces:
        spaceMesh = space.getMeshGraphic()
        model.add_triangle_mesh(spaceMesh['points'], spaceMesh['normals'], spaceMesh['indices'], 0)
    
    return {"model": model.save_base64(), "computed":{"floors":floors, "area":area}}


