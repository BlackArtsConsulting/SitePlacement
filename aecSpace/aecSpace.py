import traceback

from numpy import array
from typing import NamedTuple, List, Tuple
from uuid import uuid4

from .aecBoundary import aecBoundary
from .aecColor import aecColor
from .aecGeometry import aecGeometry
from .aecPoint import aecPoint
from .aecVertex import aecVertex

class aecSpace:
    """
    class aecSpace
    Defines the geometric enclosure of a region described by a list of 2D points,
    a level in relation to the zero plane, and a positive height in relation to the level.

    Current assumptions and limitations:

    * The XY plane is considered horizontal, the Z dimension vertical.

    * aecSpaces are prisms with bases parallel to the ground plane
      and having only vertical boundaries.

    * Curved boundaries must be represented as a series of straight segments.
    """
    
    # Defines a data structure of four vertices with locations indicated
    # by compass point abbreviations in counterclockwise order.
    
    quad_vertices = \
        NamedTuple(
        'quad_vertices',
        [
            ('ID', int),
            ('SW', aecVertex), 
            ('SE', aecVertex), 
            ('NE', aecVertex),
            ('NW', aecVertex)
        ])    

    __slots__ = \
    [ 
        '__address',
        '__boundarySet',
        '__ceiling',        
        '__color',  
        '__floor',
        '__height',
        '__ID',
        '__name',
        '__vertices_ceiling',
        '__vertices_floor',
        '__vertices_sides',
    ]
    
    __aecGeometry = aecGeometry()

    def __init__(self, points: List[aecPoint] = None, height: float = 1):
        """
        INTERNAL
        Constructor
        Sets the ID to a new UUID.
        Sets the initial color randomly.
        Sets the initial size to a 1 x 1 x 1 cube in the zero quadrant
        of the Cartesian plane with one corner at the Cartesian origin.
        """
        self.__address = (0, 0, 0)
        self.__boundarySet = False
        self.__ceiling = aecBoundary()
        self.__color = aecColor()
        self.__floor = aecBoundary()
        self.__height = float(height)
        self.__ID = str(uuid4())
        self.__name = ''        
        self.__vertices_ceiling = None
        self.__vertices_floor = None
        self.__vertices_sides = None
        if not points:
            points =\
            [
                aecPoint(0, 0, 0),
                aecPoint(1, 0, 0),
                aecPoint(1, 1, 0),
                aecPoint(0, 1, 0),
            ]
            self.__ceiling.level = 1.0
            self.__floor.level = 0.0
        self.__setBoundary(points)        

    def __setBoundary(self, points: List[aecPoint]) -> bool:
        """
        INTERNAL
        Sets the boundaries and vertices for a new set of points.
        Returns True on success.
        Returns False on failure.
        """
        try:
            self.__floor.points = points
            self.__ceiling.points = points
            flrPnts = self.__floor.points            
            clgPnts = self.__ceiling.points
            index = 0
            length = len(flrPnts)
            vertices = []
            while index < length:
                indexPre = (index - 1) % length
                indexNxt = (index + 1) % length
                vertices.append(aecVertex(flrPnts[index], flrPnts[indexPre], flrPnts[indexNxt]))
                index += 1
            self.__vertices_floor = vertices
            index = 0
            vertices = []
            while index < length:
                indexPre = (index - 1) % length
                indexNxt = (index + 1) % length                
                vertices.append(aecVertex(clgPnts[index], clgPnts[indexPre], clgPnts[indexNxt]))
                index += 1            
            self.__vertices_ceiling = vertices
            index = 0
            vertices = []          
            while index < length:
                indexPre = (index - 1) % length
                indexNxt = (index + 1) % length
                vtxSW = aecVertex(flrPnts[index], flrPnts[indexNxt], clgPnts[index])
                vtxNW = aecVertex(clgPnts[index], flrPnts[index], clgPnts[indexNxt])
                vtxNE = aecVertex(clgPnts[indexNxt], clgPnts[index], flrPnts[indexNxt])
                vtxSE = aecVertex(flrPnts[indexNxt], clgPnts[indexNxt], flrPnts[index])
                
                                
                
                
                
#                vtxSW = aecVertex(flrPnts[index], clgPnts[index], flrPnts[indexNxt])
#                vtxSE = aecVertex(flrPnts[indexNxt], flrPnts[index], clgPnts[indexNxt])
#                vtxNE = aecVertex(clgPnts[indexNxt], flrPnts[indexNxt], clgPnts[index])
#                vtxNW = aecVertex(clgPnts[index], clgPnts[indexNxt], flrPnts[index])
                vertices.append(self.quad_vertices(ID = index, 
                                                   SW = vtxSW, SE = vtxSE,
                                                   NE = vtxNE, NW = vtxNW))
                index += 1            
            self.__vertices_sides = vertices
            self.__boundarySet = True
        except Exception:
            traceback.print_exc() 
            return False  

    @property
    def address(self) -> Tuple[int, int, int]:
        """
        Property
        Returns a 3-integer address designed for use when
        the space is employed as a voxel in a grid.
        Returns None on failure.
        """
        try:
            return self.__address
        except Exception:
            traceback.print_exc() 
            return None  

    @address.setter
    def address(self, value: Tuple[int, int]):
        """
        Property
        Sets a 3-integer address designed for use when
        the space is employed as a voxel in a grid.
        """
        try:
            address = self.__address
            self.__address = value
        except Exception:
            self.__address = address
            traceback.print_exc()             

    @property
    def color(self) -> aecColor:
        """
        Property
        Returns the color.
        Returns None on failure.
        """
        try:
            return self.__color
        except Exception:
            traceback.print_exc() 
            return None

    @color.setter
    def color(self, value: Tuple[int, int, int]):
        """
        Property
        Sets the color with RGB integer values from 0 to 255.
        """
        try:
            self.__color.color = value
        except Exception:
            traceback.print_exc()  
   
    @property
    def color_alpha(self) -> int:
        """
        Property
        Returns the color as a NamedTuple.
        Returns None on failure.
        """
        try:
            return self.__color.alpha
        except Exception:
            traceback.print_exc() 
            return None

    @color_alpha.setter
    def color_alpha(self, value: int):
        """
        Property
        Sets the color with a NamedTuple containing 
        RGBA integer values from 0 to 255.
        """
        try:
            self.__color.alpha = value
        except Exception:
            traceback.print_exc()
            
    @property
    def copy_properties(self) -> dict:
        """
        Returns a dictionary with properties 
        necessary to make a copy of this space.
        """
        try:
            return \
            {
                'color': self.color.color,
                'boundary': self.floor.points,               
                'height': self.height,
                'level': self.level,
                'name': self.name,
            }
        except Exception:
            traceback.print_exc()
            return None
    
    @property
    def ceiling(self) -> aecBoundary:
        """
        Property
        Returns lower boundary.
        Returns None on failure.        
        """
        try:
            return self.__ceiling
        except Exception:
            traceback.print_exc() 
            return None           
 
    @property
    def floor(self) -> aecBoundary:
        """
        Property
        Returns lower boundary.
        Returns None on failure.        
        """
        try:
            return self.__floor
        except Exception:
            traceback.print_exc() 
            return None
 
    @floor.setter
    def boundary(self, value: List[aecPoint]):
        """
        Property
        Sets a new boundary from a list of counterclockwise points.
        Returns True on success.
        Returns False on failure.
        """
        try:
            flrPnts = self.__floor.points
            self.__setBoundary(value)
            if not self.__boundarySet: raise Exception
        except Exception:
            self.__setBoundary(flrPnts)
            traceback.print_exc() 
            return False 
          
    @property
    def height(self) -> float:
        """
        Property
        Returns the height.
        Returns None on failure.
        """
        try:
            return self.__height
        except Exception:
            traceback.print_exc() 
            return None

    @height.setter
    def height(self, value: float):
        """
        Property
        Sets the height.
        """
        try:
            preVal = self.__height
            self.__height = float(value)
            self.__ceiling.level = self.floor.level + self.__height
        except Exception:
            self.__height = preVal
            self.__ceiling.level = self.floor.level + self.__height
            traceback.print_exc()            

    @property
    def ID(self) -> str:
        """
        Property
        Returns the height.
        Returns None on failure.
        """
        try:
            return self.__ID
        except Exception:
            traceback.print_exc() 
            return None

    @property
    def level(self) -> float:
        """
        Property
        Returns the level of the lower boundary.
        Returns None on failure.
        """
        try:
            return self.__floor.level
        except Exception:
            traceback.print_exc() 
            return None
        
    @level.setter
    def level(self, value: float):
        """
        Property
        Sets the level of the lower boundary and changes the level of the 
        upper boundary to match the current difference in level values.
        Returns None on failure.
        """
        try:
            level = self.floor.level
            self.floor.level = float(value)
            self.ceiling.level = self.floor.level + self.height
            self.__setBoundary(self.floor.points)
        except Exception:
            self.floor.level = level
            self.ceiling.level = self.floor.level + self.height
            traceback.print_exc() 
            return None        

    @property
    def mesh(self) -> aecGeometry.mesh3D:
        """
        Property
        Returns a mesh of the space.
        Returns None on failure.
        """
        try:
            ceiling_mesh = self.mesh_ceiling
            vertices = ceiling_mesh.vertices
            normals = ceiling_mesh.normals
            indices = ceiling_mesh.indices
            off = len(vertices)
            floor_mesh = self.mesh_floor         
            vertices += floor_mesh.vertices
            normals += floor_mesh.normals
            indices += [(idx[0] + off, idx[1] + off, idx[2] + off) for idx in floor_mesh.indices]            
            side_meshes = self.mesh_sides
            for side in side_meshes:
                off = len(vertices)
                vertices += side.vertices
                normals += side.normals
                indices += [(idx[0] + off,idx[1] + off, idx[2] + off) for idx in side.indices] 
            return aecGeometry.mesh3D(vertices = vertices, 
                                      indices = indices, 
                                      normals = normals)                      
        except Exception:
            traceback.print_exc() 
            return None  

    @property
    def mesh_ceiling(self) -> aecGeometry.mesh2D:
        """
        Property
        Returns a mesh of the upper surface.
        Returns None on failure.
        """
        try:
            mesh2D = self.__aecGeometry.getMesh2D(self.ceiling.points)
            vertices = [(vtx[0], vtx[1], self.ceiling.level) for vtx in mesh2D.vertices]
            normal = self.normal_ceiling
            normals = []
            for vertex in vertices: normals.append(normal)
            return self.__aecGeometry.mesh3D(vertices = mesh2D.vertices,
                                             indices = mesh2D.indices,
                                             normals = normals)
        except Exception:
            traceback.print_exc() 
            return None   

    @property
    def mesh_floor(self) -> aecGeometry.mesh3D:
        """
        Property
        Returns a mesh of the lower surface.
        Returns None on failure.
        """
        try:
            mesh2D = self.__aecGeometry.getMesh2D(self.floor.points)
            vertices = mesh2D.vertices
            normal = self.normal_floor
            normals = []
            for vertex in vertices: normals.append(normal)
            return self.__aecGeometry.mesh3D(vertices = mesh2D.vertices[::-1],
                                             indices = mesh2D.indices,
                                             normals = normals)
        except Exception:
            traceback.print_exc() 
            return None       
        
    @property
    def mesh_graphic(self) -> aecGeometry.mesh3Dgraphic:
        """
        Property
        Returns a mesh of the space as sequences of floats.
        Returns None on failure.
        """
        try:
            space_mesh = self.mesh
            vertices = []
            indices = []
            normals = []
            for item in space_mesh.vertices: vertices += [item[0], item[1], item[2]]
            for item in space_mesh.indices: indices += [item[0], item[1], item[2]]
            for item in space_mesh.normals: normals += [item[0], item[1], item[2]]
            return aecGeometry.mesh3Dgraphic(vertices = vertices, 
                                             indices = indices, 
                                             normals = normals)
        except Exception:
            traceback.print_exc() 
            return None   

    @property
    def mesh_sides(self) -> List[aecGeometry.mesh2D]:
        """
        Property
        Returns a mesh of the upper surface.
        Returns None on failure.
        """
        try:
            sides = self.points_sides
            normals = self.normal_sides
            meshes = []
            index = 0
            for side in sides:
               side_vertices = [side.SW.xyz, side.SE.xyz, side.NE.xyz, side.NW.xyz]
               side_indices = [(1, 2, 3), (0, 1, 3)]
               side_normals = []
               for vertex in side_vertices: side_normals.append(normals[index])
               meshes.append(aecGeometry.mesh3D(vertices = side_vertices,
                                                indices = side_indices,
                                                normals = side_normals))
               index += 1
            return meshes
        except Exception:
            traceback.print_exc() 
            return None  

    @property
    def name(self) -> str:
        """
        Property
        Returns the name.
        Returns None on failure.
        """
        try:
            return self.__name
        except Exception:
            traceback.print_exc() 
            return None

    @name.setter
    def name(self, value: str):
        """
        Property
        Sets the name.
        """
        try:
            name = self.__name
            self.__name = str(value)
        except Exception:
            self.__name = name
            traceback.print_exc() 

    @property
    def normal_ceiling(self) -> Tuple[int, int, int]:
        """
        Property
        Returns the list of point normals from each vertex.
        Returns None on failure.
        """
        try:
            normals = [vertex.normal_array for vertex in self.__vertices_ceiling]
            return self.__aecGeometry.getNormalSurface(normals)
        except Exception:
            traceback.print_exc() 
            return None 
       
    @property
    def normals_ceiling(self) -> List[Tuple[int, int, int]]:
        """
        Property
        Returns the list of point normals from each vertx.
        Returns None on failure.
        """
        try:
            return [vertex.normal for vertex in self.__vertices_ceiling]
        except Exception:
            traceback.print_exc() 
            return None         

    @property
    def normal_floor(self) -> Tuple[int, int, int]:
        """
        Property
        Returns the surface normal of the floor.
        Returns None on failure.
        """
        try:
            normals = [vertex.normal_array for vertex in self.__vertices_floor]
            return self.__aecGeometry.getNormalSurface(normals)
        except Exception:
            traceback.print_exc() 
            return None      

    @property
    def normals_floor(self) -> List[array]:
        """
        Property
        Returns the list of point normals from each vertex.
        Returns None on failure.
        """
        try:
            return [vertex.normal for vertex in self.__vertices_floor]
        except Exception:
            traceback.print_exc() 
            return None

    @property
    def normal_sides(self) -> List[array]:
        """
        Property
        Returns the list of surface normals from each side.
        Returns None on failure.
        """
        try:
            norm_sides = []
            for side in self.normals_sides: 
                norm_sides.append(self.__aecGeometry.getNormalSurface(side))
            return norm_sides
        except Exception:
            traceback.print_exc() 
            return None   
        
    @property
    def normals_sides(self) -> List[List[array]]:
        """
        Property
        Returns the list of surface normals from each side.
        Returns None on failure.
        """
        try:
            norm_sides = []
            for side in self.__vertices_sides:
                norm_sides.append(
                [
                    side.SW.normal,
                    side.SE.normal,
                    side.NE.normal,
                    side.NW.normal,
                ])
            return norm_sides
        except Exception:
            traceback.print_exc() 
            return None          

    @property
    def points_sides(self) -> List[aecGeometry.quad_points]:
        """
        Property
        Returns a list of quad structures of 
        four points defining each side.
        Returns None on failure.
        """
        try:
            side_points = []
            index = 0
            for vtx in self.__vertices_sides:
               side_points.append(aecGeometry.quad_points(ID = index,
                                                          SW = vtx.SW.point,
                                                          SE = vtx.SE.point,
                                                          NE = vtx.NE.point,
                                                          NW = vtx.NW.point))
               index += 1
            return side_points
        except Exception:
            traceback.print_exc() 
            return None            

    @property
    def volume(self) -> float:
        """
        Property
        Returns the volume.
        Returns None on failure.
        """
        try:
            return self.__height * self.__floor.area
        except Exception:
            traceback.print_exc() 
            return None

    def addBoundary(self, points: List[aecPoint], restart: bool = False) -> bool:
        """
        If restart is True, constructs a new boundary from the delivered list of points.
        If restart is False, combines the current boundary with boundaries defined by
        the delivered points.
        Returns True if successful.        
        Returns False if the delivered points do not resolve to a single non-crossing
        polygon and leaves the current boundary unchanged.
        """
        try:
            points = self.__floor.points
            if not self.__floor.add(points, restart): raise Exception
            self.__setBoundary(self.__floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False

    def enclosesBoundary(self, boundary: aecBoundary) -> bool:
        """
        Returns True if the delivered boundary falls within the space,
        respecting the boundary and level of the space relative to
        point positions, returning False if the points fall outside
        the space.
        Returns None on failure.
        """
        try:
            return self.__floor.containsShape(boundary.points) and \
                   boundary.level >= self.level
        except Exception:
            traceback.print_exc()
            return None   

    def enclosesPoint(self, point: aecPoint) -> bool:
        """
        Returns True if the delivered point falls within the space,
        respecting the boundary and level of the space relative to
        the point's position, returning False if the point is outside
        the space.
        Returns None on failure.
        """
        try:
            return self.__polygon.containsPoint(point) and \
                   point.z >= self.level and \
                   point.z <= (self.level + self.height)
        except Exception:
            traceback.print_exc()
            return None
        
    def enclosesSpace(self, boundary: aecBoundary, height: float) -> bool:
        """
        Returns True if the delivered boundary and height fall within the space,
        respecting the boundary, level, and height of the space relative
        to the point positions, returning False if the points fall outside
        the space.
        Returns None on failure.
        """
        try:
            return self.__floor.containsShape(boundary.points) and \
                   boundary.level >= self.level and \
                   height <= self.height
        except Exception:
            traceback.print_exc()
            return None           

    def fitWithin(self, points: List[aecPoint] = None) -> bool:
        """
        Moves the space by the delivered x, y, and z displacements.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.__floor.points
            if not self.__floor.fitWithin(points): raise Exception
            self.__setBoundary(self.__floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False

    def makeBox(self, origin: aecPoint, xDist: float = 1, yDist: float = 1, zDist: float = 1) -> bool:
        """
        Creates a rectangular space constructed from an
        origin point and a diagonally opposite point.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.__floor.points
            level = self.level
            height = self.height
            self.level = origin.z
            self.height = zDist
            if not self.__floor.makeBox(origin, xDist, yDist): raise Exception
            self.__setBoundary(self.__floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            self.level = level
            self.height = height            
            traceback.print_exc()
            return False

    def makeCross(self, origin: aecPoint = aecPoint(0, 0, 0), 
                        xSize: float = 1, ySize: float = 1,
                        xWidth: float = 0.33333333, yDepth: float = 0.33333333,
                        xAxis: float = 0.5, yAxis: float = 0.5) -> bool:
        """
        Constructs a cross-shaped space within the box defined by the origin and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each cross arm.
        xAxis and yAxis are percentages of overall x-axis and y-axis distances that
        determine the centerline of each cross arm.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.floor.makeCross(origin, xSize, ySize, xWidth, yDepth, xAxis, yAxis):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False

    def makeCylinder(self, origin: aecPoint = aecPoint(0, 0, 0), radius = 1) -> bool:
        """
        Contructs the space as an approximate circle, setting 
        a ratio from the delivered radius to the number of sides.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.floor.makeCylinder(origin, radius):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False
        
    def makeH(self, origin: aecPoint = aecPoint(0, 0, 0),
                    xSize: float = 1, ySize: float = 1,
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333) -> bool:
        """
        Constructs an H-shaped space within the box defined by point and xy deltas.
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:            
            if self.floor.makeH(origin, xSize, ySize, xWidth1, xWidth2, yDepth):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False

    def makeL(self, origin: aecPoint = aecPoint(0, 0, 0), 
                    xSize: float = 1, ySize: float = 1,
                    xWidth = 0.33333333, yDepth = 0.33333333) -> bool:
        """
        Constructs a L-shaped space within the box defined by point and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances
        that determine the width of each bar.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.floor.makeL(origin, xSize, ySize, xWidth, yDepth):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False
        
    def makePolygon(self, origin: aecPoint = aecPoint(0, 0, 0), radius = 1, sides = 3) -> bool:
        """
        Constructs the space as a regular polygon centered on the delivered
        origin point with the first vertex at the maximum y-coordinate.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.floor.makePolygon(origin, radius, sides):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False       
        
    def makeT(self, origin = aecPoint(0, 0, 0), 
                    xSize: float = 1, ySize: float = 1,
                    xWidth = 0.33333333, yDepth = 0.33333333) -> bool:
        """
        Constructs a T-shaped space within the box defined by point and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of the vertical and horizonatl bars, respectively.
        Returns True on success.
        Returns False on failure.
        """        
        try:
            if self.floor.makeT(origin, xSize, ySize, xWidth, yDepth):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False
        
    def makeU(self, origin = aecPoint(0, 0, 0),
                    xSize: float = 1, ySize: float = 1,
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333):
        """
        Constructs a U-shaped boundary within the box defined by point and xy deltas.
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances
        that determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.floor.makeU(origin, xSize, ySize, xWidth1, xWidth2, yDepth):
                self.__setBoundary(self.floor.points)            
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False       
   
    def mirror(self, points: List[aecPoint] = None) -> bool:
        """
        Moves the space by the delivered x, y, and z displacements.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.floor.points
            if not self.floor.mirror(points): raise Exception
            self.__setBoundary(self.floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False         

    def moveBy(self, x: float = 0, y: float = 0, z: float = 0) -> bool:
        """
        Moves the space by the delivered x, y, and z displacements.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.floor.points
            if not self.floor.moveBy(x, y): raise Exception
            self.level += z            
            self.__setBoundary(self.floor.points)
                        
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False  

    def moveTo(self, fromPnt: aecPoint, toPnt: aecPoint) -> bool:
        """
        Attempts to move the space by constructing a vector between the "from" and "to" points.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.floor.points
            if not self.floor.moveTo(fromPnt, toPnt): raise Exception
            self.__setBoundary(self.floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False    

    def rotate(self, angle: float, point: aecPoint = None):
        """
        Rotates the space by the delivered angle in degrees.
        If no point is provided, the space will scale from its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.__floor.points
            if not self.__floor.rotate(angle, point): raise Exception
            self.__setBoundary(self.__floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False      
        
    def scale(self, x: float = 1, y: float = 1, z: float = 1, point: aecPoint = None):
        """
        Scales the space by the delivered x, y, and z factors.
        If no point is provided, the space will scale from its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.__floor.points
            if not self.__floor.scale(x, y, point): raise Exception
            self.__height *= float(z)
            self.__setBoundary(self.__floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False       
        
    def wrap(self, points: List[aecPoint]) -> bool:
        """
        Sets the space to a convex hull derived
        from the delivered list of points.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            points = self.__floor.points
            if not self.__floor.wrap(points): raise Exception
            self.__setBoundary(self.__floor.points)
            return self.__boundarySet
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False  