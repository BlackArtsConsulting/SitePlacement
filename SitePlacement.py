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
        [1771.8803, 1282.6400],       
        [1792.2478, 1263.0727],      
        [2108.5229, 1263.0727],      
        [2700.4829, 1737.8546],
        [2700.4829, 2289.2733],
        [2000.1994, 2289.2733],
     ]
}
  
def makeBuilding(site: aecSpace, length: float, width: float, height: float, 
                                 rotation: float, area: float):
    spacer = aecSpacer()
    building = aecSpace()
    building.makeBox(aecPoint(0, 0, 0), xSize = length, ySize = width, zSize = height)
    building.rotate(rotation)
    if spacer.placeWithin(building, site):
        building.level = 0
        building.height = height
        building = [building]
        building += spacer.stackToArea(building[0], area) 
    return building
    
def makeSite():
    site = aecSpace()
    site.points_floor = [aecPoint(coord[0], coord[1]) for coord in siteBoundary["coordinates"]]
    site.color = aecColor.green
    site.level = -20
    site.height = 20 
    return site     

def sitePlacement(length: float, width: float, height: float, 
                  rotation: float, area: float):
    site = makeSite()
    building = makeBuilding(site, length, width, height, rotation, area)
    area = 0
    floors = 0
    for space in building:
        area += space.area
        floors += 1
    model = glTF()
    colorBlue = model.add_material(0.0, 0.631, 0.945, 0.9, 1.0, "Blue")
    colorGreen = model.add_material(0.486, 0.733, 0.0, 0.9, 0.0, "Green")
    colorOrange = model.add_material(0.964, 0.325, 0.078, 0.9, 1.0, "Orange")
    colorYellow = model.add_material(1.0, 0.733, 0.0, 0.9, 1.0, "Yellow")
    spaceMesh = site.mesh_graphic
    model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, colorGreen)
    for space in building:
        spaceMesh = space.mesh_graphic
        colorIndex = random.randint(0, 2)
        if colorIndex == 0: color = colorBlue
        if colorIndex == 1: color = colorOrange
        if colorIndex == 2: color = colorYellow      
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, color)   
    return {"model": model.save_base64(), 'computed':{'floors':floors, 'area':area}}   
#    model.save_glb('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\SitePlacement\\model.glb')
#
#sitePlacement(length = random.uniform(200, 400), 
#              width = random.uniform(200, 300), 
#              height = random.uniform(20, 40),
#              rotation = random.uniform(5, 355), 
#              area = random.uniform(80000, 150000))




