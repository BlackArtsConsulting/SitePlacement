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
  
def makeBuilding(site: aecSpace, width: float, rotation: float, area: float):
    spacer = aecSpacer()
#    xWidth = buildings[0]['diameter'][random.randint(0, 0)]
    yDepth = width * 1.618
    building = aecSpace()
    building.makeBox(aecPoint(0, 0, 0), xDist = width, yDist = yDepth, zDist = 40)
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

def sitePlacement(width: float, rotation: float, area: float):
    
#    site = aecSpace()
#    site.boundary = [aecPoint(coord[0], coord[1]) for coord in siteBoundary["coordinates"]]
#    site.color = aecColor.green
#    site.level = -0.1
#    site.height = 0.1
#    spaces = []
#    xWidth = buildings[0]['diameter'][random.randint(0, 0)]
#    yDepth = xWidth * 1.618
#    building = aecSpace()
#    building.makeBox(aecPoint(0, 0, 0), xDist = xWidth, yDist = yDepth, zDist = 10)
#    building.rotate(random.randint(0, 360))
#    if spacer.placeWithin(building, site):
#        building.height = buildings[0]['height']
#        building.level = buildings[0]['level']
#        building.color = buildings[0]['color']
#        spaces += [building]
#        spaces += spacer.stackToArea(building, buildings[0]['area'])
    site = makeSite()
    building = makeBuilding(site, width, rotation, area)
    area = 0
    floors = 0
    for space in building:
        area += space.floor.area
        floors += 1
        
    # Create a model to hold the geometry.
    model = glTF()

    # Create materials to use in the model.
    m_index = model.add_material(0.0, 0.0, 1.0, 0.9, 1.0, "Blue")
    m_index1 = model.add_material(0.0, 1.0, 0.0, 0.9, 1.0, "Green")

    spaceMesh = site.mesh_graphic
    model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, m_index1)
    
    for space in building:
        spaceMesh = space.mesh_graphic
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, m_index)
        
#        print(spaceMesh.vertices)
#        for item in spaceMesh.vertices: print(type(item))
#        print(len(spaceMesh.vertices))
#        print(spaceMesh.normals)
#        for item in spaceMesh.normals: print(type(item))        
#        print(len(spaceMesh.normals))        
#        print(spaceMesh.indices)
#        for item in spaceMesh.indices: print(type(item))        
#        print(len(spaceMesh.indices))        
#        print(min(spaceMesh.normals))
#        print(max(spaceMesh.normals))
#        for item in spaceMesh.normals: print(item)
#        
        
    return {"model": model.save_base64(), 'computed':{'floors':floors, 'area':area}}        
    
#    model.save('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\SitePlacement\\model.gltf')
#    model.save_glb('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\SitePlacement\\model.glb')
    

    
# sitePlacement(random.uniform(150, 300), random.uniform(5, 355), random.uniform(100000, 200000))




