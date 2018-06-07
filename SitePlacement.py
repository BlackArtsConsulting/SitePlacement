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
  
def makeBuilding(site: aecSpace, length: float, width: float, height: float, 
                                 rotation: float, area: float):
    spacer = aecSpacer()
    yDepth = width * 1.618
    building = aecSpace()
    building.makeBox(aecPoint(0, 0, 0), xDist = width, yDist = yDepth, zDist = 40)
#    building.makePolygon(radius = 100, sides = 5)
    building.rotate(rotation)
    if spacer.placeWithin(building, site):
        building.level = 0
        building.height = buildings[0]['height']
        building = [building]
        building += spacer.stackToArea(building[0], area) 
    return building
    
def makeSite():
    site = aecSpace()
    site.boundary = [aecPoint(coord[0], coord[1]) for coord in siteBoundary["coordinates"]]
    site.color = aecColor.green
    site.level = -0.1
    site.height = 0.1 
    return site     

def sitePlacement(length: float, width: float, height: float, 
                  rotation: float, area: float):
    site = makeSite()
    site.moveBy(0, 0, 0)
    building = makeBuilding(site, length, width, height, rotation, area)
    area = 0
    floors = 0
    for space in building:
        area += space.floor.area
        floors += 1
    model = glTF()
    colorBlue = model.add_material(0.0, 0.631, 0.945, 0.9, 1.0, "Blue")
    colorGreen = model.add_material(0.486, 0.733, 0.0, 0.9, 0.0, "Green")
    colorOrange = model.add_material(0.964, 0.325, 0.078, 0.9, 1.0, "Orange")
    colorYellow = model.add_material(1.0, 0.733, 0.0, 0.9, 1.0, "Yellow")
    spaceMesh = site.mesh_graphic
    model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, colorGreen)
    for space in building:
        space.moveBy(0, 0, 0)
        spaceMesh = space.mesh_graphic
        colorIndex = random.randint(0, 2)
        if colorIndex == 0: color = colorBlue
        if colorIndex == 1: color = colorOrange
        if colorIndex == 2: color = colorYellow      
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, color)   
#    model.save_glb('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\SitePlacement\\model.glb')
    return {"model": model.save_base64(), 'computed':{'floors':floors, 'area':area}}   

#sitePlacement(length = random.uniform(200, 300), 
#              width = random.uniform(100, 300), 
#              height = random.uniform(20, 40),
#              rotation = random.uniform(5, 355), 
#              area = random.uniform(100000, 200000))




