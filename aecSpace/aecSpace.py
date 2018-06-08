import math
import traceback

from random import uniform
from typing import List, Tuple
from uuid import uuid4

from shapely import geometry as shapely
from shapely import affinity as shapelyAffine
from shapely import ops as shapelyOps

from .aecColor import aecColor
from .aecGeometry import aecGeometry
from .aecPoint import aecPoint

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
    __aecGeometry = aecGeometry()
    __slots__ = \
    [
         '__address',
         '__color',           
         '__convex',
         '__height',
         '__ID',
         '__level',
         '__name',
         '__points_floor',
         '__polygon',
    ]   

    def __init__(self, points: List[aecPoint] = None):
        """
        Constructor defaults to a 1 x 1 square with an origin at (0, 0, 0).
        The first delivered point is examined for its z coordinate and all
        z coordinates are normalized to that value.
        """
        self.__address = (0, 0, 0)
        self.__color = aecColor()
        self.__height = 1.0
        self.__ID = str(uuid4())
        self.__level = 0.0
        self.__name = ''
        self.__points_floor = None
        if not points:
            points = \
            [
                aecPoint(0, 0), 
                aecPoint(1, 0), 
                aecPoint(1, 1), 
                aecPoint(0, 1)
            ]
        self.__setBoundary(points)

    def __setBoundary(self, points: List[aecPoint]) -> bool:
        """
        Creates a boundary from a set of counterclockwise points.
        """
        try:
            prePoints = self.__points_floor
            points = self.__aecGeometry.rmvColinear(points)
            if len(points) < 3: raise ValueError('Need at least three non-colinear points')                
            polygon = shapely.polygon.orient(shapely.Polygon([point.xy for point in points]))
            if type(polygon) != shapely.polygon.Polygon: raise Exception
            self.__points_floor =  points = [aecPoint(pnt[0], pnt[1]) for pnt in polygon.exterior.coords[:-1]] 
            self.__polygon = polygon
            self.__convex = self.__aecGeometry.isConvex(points)
        except Exception:
            self.__points_floor = prePoints
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
    def area(self) -> float:
        """
        Returns the area of the boundary.
        Returns None on failure.
        """
        try:
            return self.__polygon.area
        except:
            traceback.print_exc() 
            return None        
    
    @property
    def axis_major(self) -> List[aecPoint]:
        """
        Returns the longer of the two orthogonal bounding box axes as two endpoints.
        If both axes are the same length, returns the x-axis endpoints.
        Returns None on failure.
        """
        try:
            box = self.points_box
            xDelta = abs(box.SE.x - box.SW.x)
            yDelta = abs(box.NE.y - box.SE.y)   
            if xDelta >= yDelta: return self.axis_x
            else: return self.axis_y
        except:
            traceback.print_exc() 
            return None 

    @property
    def axis_minor(self) -> List[aecPoint]:
        """
        Returns the shorter of the two orthogonal bounding box axes as two endpoints.
        If both axes are the same length, returns the y-axis endpoints.
        Returns None on failure.
        """
        try:
            box = self.points_box
            xDelta = abs(box.SE.x - box.SW.x)
            yDelta = abs(box.NE.y - box.SE.y)   
            if xDelta < yDelta: return self.axis_x
            else: return self.axis_y
        except:
            traceback.print_exc() 
            return None             

    @property
    def axis_x(self) -> List[aecPoint]:
        """
        Returns the central x-axis of the bounding box as two endpoints.
        Rerurns None on failure.
        """
        try:
            box = self.points_box
            return [self.__aecGeometry.getMidpoint(box.SW, box.NW),
                    self.__aecGeometry.getMidpoint(box.SE, box.NE)]
        except:
            traceback.print_exc() 
            return None 

    @property
    def axis_y(self) -> List[aecPoint]:
        """
        Returns the central y-axis of the bounding box as two endpoints.
        Rerurns None on failure.
        """
        try:
            box = self.points_box
            return [self.__aecGeometry.getMidpoint(box.SW, box.SE),
                    self.__aecGeometry.getMidpoint(box.NW, box.NE)]
        except:
            traceback.print_exc() 
            return None              
    
    @property
    def box(self) -> shapely.Polygon:
        """
        Returns a polygon of the boundary's bounding box.
        Returns None on failure.        
        """
        try:
            bounds = self.__polygon.bounds
            return shapely.polygon.orient(
                   shapely.Polygon(
                   [
                       (bounds[0], bounds[1]),
                       (bounds[2], bounds[1]),
                       (bounds[2], bounds[3]),
                       (bounds[0], bounds[3])
                   ]))
        except:
            traceback.print_exc() 
            return None  

    @property
    def center_floor(self) -> aecPoint:
        """
        Returns the center of the bounding box.
        Returns None on failure.
        """
        try:
            box_pnts = self.points_box
            point = self.__aecGeometry.getMidpoint(box_pnts.SW, box_pnts.NE)
            point.z = self.level
            return point
        except:
            traceback.print_exc() 
            return None 

    @property
    def center_space(self) -> aecPoint:
        """
        Returns the center of the space determined as the
        halfway point between the ceiling and floor centers.
        """
        try:
            flrCenter = self.center_floor
            flrCenter.z = self.boundary.level + (self.height * 0.5)
        except Exception:
            traceback.print_exc() 
            return None     

    @property
    def centroid_ceiling(self) -> aecPoint:
        """
        Returns the centroid of the boundary.
        Returns None on failure.
        """
        try:
            centroid = self.__polygon.centroid    
            return aecPoint(centroid.x, centroid.y, self.points_ceiling[0].z)
        except:
            traceback.print_exc() 
            return None 

    @property
    def centroid_floor(self) -> aecPoint:
        """
        Returns the centroid of the boundary.
        Returns None on failure.
        """
        try:
            centroid = self.__polygon.centroid    
            return aecPoint(centroid.x, centroid.y, self.points_floor[0].z)
        except:
            traceback.print_exc() 
            return None 
        
    @property
    def centroid_space(self) -> aecPoint:
        """
        Returns the centroid of the boundary.
        Returns None on failure.
        """
        try:
            centroid = self.__polygon.centroid    
            return aecPoint(centroid.x, centroid.y, (self.points_floor[0].z + (self.height * 0.5)))
        except:
            traceback.print_exc() 
            return None         
        
    @property
    def circumference(self) -> float:
        """
        Returns the length of the boundary.
        Returns None on failure.
        """
        try:
            return self.__polygon.length
        except:
            traceback.print_exc() 
            return None             

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
                'boundary': self.points_floor,                               
                'color': self.color.color,
                'height': self.height,
                'level': self.level,
                'name': self.name,
            }
        except Exception:
            traceback.print_exc()
            return None
 
    @property
    def convex(self) -> bool:
        """
        Property
        Returns the convex state of the boundary.
        Returns None on failure.        
        """
        try:
            return self.__convex
        except:
            traceback.print_exc() 
            return None

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
        except Exception:
            self.__height = preVal
            self.__ceiling.level = self.floor.level + self.__height
            traceback.print_exc()   

    @property
    def ID(self) -> str:
        """
        Property
        Returns the UUID.
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
        Returns the level of the boundary.
        Returns None on failure.
        """
        try:
            return self.__level
        except:
            traceback.print_exc() 
            return None        
 
    @level.setter
    def level(self, value: float):
        """
        Property
        Sets the level of the boundary.
        """        
        try:
            preVal = self.__level
            self.__level = float(value)
        except:
            self.__level = preVal
            traceback.print_exc() 

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
            indices = ceiling_mesh.indices     
            normals = ceiling_mesh.normals
            off = len(vertices)
            floor_mesh = self.mesh_floor
            vertices += floor_mesh.vertices
            normals += floor_mesh.normals
            indices += [(idx[0] + off, idx[1] + off, idx[2] + off) for idx in floor_mesh.indices[::-1]]            
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
    def mesh_ceiling(self) -> aecGeometry.mesh3D:
        """
        Property
        Returns a Delaunay mesh of points and indices.
        Returns None on failure.
        """
        try:
            mesh2D = self.__aecGeometry.getMesh2D(self.points_ceiling)
            vertices = mesh2D.vertices
            normal = self.normal_ceiling
            normals = []
            for vertex in vertices: normals.append(normal)
            return self.__aecGeometry.mesh3D(vertices = mesh2D.vertices,
                                             indices = mesh2D.indices,
                                             normals = normals)            
        except:
            traceback.print_exc() 
            return None
        
    @property
    def mesh_floor(self) -> aecGeometry.mesh3D:
        """
        Property
        Returns a Delaunay mesh of points and indices.
        Returns None on failure.
        """
        try:
            mesh2D = self.__aecGeometry.getMesh2D(self.points_floor)
            vertices = mesh2D.vertices[::-1]
            indices = mesh2D.indices[::-1]
            normal = self.normal_floor
            normals = []
            for vertex in vertices: normals.append(normal)
            return self.__aecGeometry.mesh3D(vertices = vertices,
                                             indices = indices,
                                             normals = normals)            
        except:
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
               side_vertices = [pnt.xyz for pnt in side]
               side_indices = [(0, 1, 2), (2, 3, 0)]
               side_normals = []
               for pnt in side: side_normals.append(normals[index])
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
    def normal_ceiling(self) -> Tuple[float, float, float]:
        """
        Property
        Returns the level of the boundary.
        Returns None on failure.
        """
        try:
            return (0.0, 0.0, 1.0)
        except:
            traceback.print_exc() 
            return None 
        
    @property
    def normal_floor(self) -> Tuple[float, float, float]:
        """
        Property
        Returns the level of the boundary.
        Returns None on failure.
        """
        try:
            return (0.0, 0.0, -1.0)
        except:
            traceback.print_exc() 
            return None        
             
    @property
    def normal_sides(self) -> List[Tuple[float, float, float]]:
        """
        Property
        Returns the list of surface normals from each side.
        Returns None on failure.
        """
        try:
            normals = []
            for side in self.points_sides:
                normals.append(self.__aecGeometry.getNormal(side[0], side[3], side[1]))
            return normals
        except Exception:
            traceback.print_exc() 
            return None                  

    @property
    def points_box(self) -> aecGeometry.quad_points:
        """
        Returns the aecPoints defining the corners of
        the bounding box at the boundary's level.
        Returns None on failure.        
        """
        try:
            bounds = self.__polygon.bounds
            level = self.__points_floor[0].z
            return aecGeometry.quad_points(ID = 0,
                                           SW = aecPoint(bounds[0], bounds[1], level),
                                           SE = aecPoint(bounds[2], bounds[1], level),
                                           NE = aecPoint(bounds[2], bounds[3], level),
                                           NW = aecPoint(bounds[0], bounds[3], level),
                                           normal = self.normal_floor)
        except:
            traceback.print_exc() 
            return None
    
    @property
    def points_ceiling(self) -> List[aecPoint]:
        """
        Returns a ceiling boundary.
        """
        try:
            return [aecPoint(pnt.x, pnt.y, self.level + self.height) 
                    for pnt in self.points_floor]
        except Exception:
            traceback.print_exc()
            return None

    @property
    def points_floor(self) -> List[aecPoint]:
        """
        Property
        Returns the points defining the boundary as an aecPoint list in a counterclockwise sequence.
        Returns None on failure.
        """
        try:
            return [aecPoint(pnt.x, pnt.y, self.level) for pnt in self.__points_floor]
        except:
            traceback.print_exc() 
            return None

    @points_floor.setter
    def points_floor(self, points: List[aecPoint]):
        """
        Create a new boundary polygon from the list of points.
        Colinear points are removed. Fails if a single 
        non-crossing polygon cannot be contructed.
        """
        try:
            self.__setBoundary(points)
        except Exception:
            traceback.print_exc()
            
    @property
    def points_sides(self) -> List[List[aecPoint]]:
        """
        Property
        Returns a list of lists of four points defining each side.
        Returns None on failure.
        """
        try:
            flrPnts = self.points_floor
            clgPnts = self.points_ceiling            
            sides = []
            index = 0
            length = len(flrPnts)
            while index < length:
                indexNxt = (index + 1) % length
                sides.append([flrPnts[index], flrPnts[indexNxt], clgPnts[indexNxt], clgPnts[index]])
                index += 1
            return sides
        except Exception:
            traceback.print_exc() 
            return None    

    @property
    def polygon(self) -> shapely.Polygon:
        """
        Returns a polygon representating the boundary.
        Returns None on failure.        
        """
        try:
            return self.__polygon
        except:
            traceback.print_exc() 
            return None

    @property
    def size_x(self) -> float:
        """
        Property
        Returns the x-axis size of the bounding box.
        Returns None on failure.
        """
        try:
            points = self.points_box
            return abs(points.SE.x - points.SW.x)
        except:
            traceback.print_exc() 
            return None  
        
    @property
    def size_y(self) -> float:
        """
        Property
        Returns the x-axis size of the bounding box.
        Returns None on failure.
        """
        try:
            points = self.points_box
            return abs(points.NW.y - points.SW.y)
        except:
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
            return self.height * self.area
        except Exception:
            traceback.print_exc() 
            return None            


    def add(self, points: List[aecPoint], restart: bool = False) -> bool:
        """
        If restart is True, constructs a new boundary from the delivered list of points.
        If restart is False, combines the current boundary with boundaries defined by
        the delivered points.
        Returns False if the delivered points do not resolve to a single non-crossing
        polygon and leaves the current boundary unchanged.
        Returns True if successful.
        """
        try:
            if restart: boundaries = []
            else: boundaries = [self.__polygon]
            self.__setBoundary(points)
            if self.__boundarySet:
                boundaries.append(self.__polygon)
                boundaries = shapely.MultiPolygon(boundaries)
                boundary = shapelyOps.unary_union(boundaries)
                if type(boundary) != shapely.polygon.Polygon: return False
                points = [aecPoint(pnt[0], pnt[1]) for pnt in list(boundary.exterior.coords)[:-1]]
                self.__setBoundary(points)
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False

    def compassLine(self, orient: int = aecGeometry.N) -> aecPoint:
        """
        Returns a point on the bounding box aligned 
        with one of 16 cardinal divisions on the box.
        Returns None on failure.
        """
        try:
            return aecGeometry.getCompassLine(self.points_box, orient)
        except Exception:
            traceback.print_exc()
            return None 

    def compassPoint(self, orient: int = aecGeometry.N) -> aecPoint:
        """
        Returns a point on the bounding box aligned 
        with one of 16 cardinal divisions on the box.
        Returns None on failure.
        """
        try:
            return aecGeometry.getCompassPoint(self.points_box, orient)
        except Exception:
            traceback.print_exc()
            return None         

    def containsPoint(self, point: aecPoint) -> bool:
        """
        Returns True if the boundary contains the point on the shared zero plane.
        Returns None on failure.
        """
        try:
            return self.__polygon.contains(shapely.Point(point.x, point.y))
        except Exception:
            traceback.print_exc()
            return None

    def containsShape(self, points: List[aecPoint]) -> bool:
        """
        Returns True if the boundary wholly contains the shape on the shared zero plane.
        Returns None on failure.
        """
        try:
            shape_points = [pnt.xy for pnt in points]
            shape = shapely.polygon.orient(shapely.Polygon(shape_points))
            return self.__polygon.contains(shape)
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
        
#    def enclosesSpace(self, boundary: aecSpace, height: float) -> bool:
#        """
#        Returns True if the delivered boundary and height fall within the space,
#        respecting the boundary, level, and height of the space relative
#        to the point positions, returning False if the points fall outside
#        the space.
#        Returns None on failure.
#        """
#        try:
#            return self.__floor.containsShape(boundary.points) and \
#                   boundary.level >= self.level and \
#                   height <= self.height
#        except Exception:
#            traceback.print_exc()
#            return None           

#    def fitWithin(self, points: List[aecPoint] = None) -> bool:
#        """
#        Moves the space by the delivered x, y, and z displacements.
#        Returns True on success.
#        Returns False on failure.
#        """
#        try:
#            prePoints = self.__floor.points
#            if not self.__floor.fitWithin(points): raise Exception
#            self.__setBoundary(self.__floor.points)
#            return self.__setBoundary
#        except Exception:
#            self.__setBoundary(prePoints)
#            traceback.print_exc()
#            return False

#    def fitWithin(self, points: List[aecPoint]):
#        """
#        If the boundary is not wholly within the delivered perimeter as
#        described in a list of points, the boundary reconfigures to fit
#        within the delivered perimeter.
#        Returns True on success.
#        Returns None on failure.
#        """
#        try:
#            intersect = self.__aecGeometry.getIntersect(self.points, points)
#            if intersect: self.__setBoundary(intersect)
#            return self.__boundarySet
#        except Exception:
#            traceback.print_exc()
#            return None
    
    def makeBox(self, origin: aecPoint, 
                      xSize: float = 1.0, ySize: float = 1.0, zSize: float = 1.0) -> bool:
        """
        Creates a rectangular boundary from two diagonal points.
        """
        try:
            return self.__setBoundary([aecPoint(origin.x, origin.y),
                                       aecPoint(origin.x + xSize, origin.y),
                                       aecPoint(origin.x + xSize, origin.y + ySize),
                                       aecPoint(origin.x, origin.y + ySize)])
        except Exception:
            traceback.print_exc()
            return False    

    def makeCross(self, origin: aecPoint = aecPoint(0, 0, 0), 
                        xSize: float = 1, ySize: float = 1,
                        xWidth: float = 0.33333333, yDepth: float = 0.33333333,
                        xAxis: float = 0.5, yAxis: float = 0.5) -> bool:
        """
        Constructs a cross-shaped boundary within the box defined by the origin and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each cross arm.
        xAxis and yAxis are percentages of overall x-axis and y-axis distances that
        determine the centerline of each cross arm.
        Returns True on success.
        Returns False on failure.
        """
        try:
            xWidth = self.__aecValid.validPercent(xWidth) * xSize
            yDepth = self.__aecValid.validPercent(yDepth) * ySize
            xAxis = self.__aecValid.validPercent(xAxis) * xSize
            yAxis = self.__aecValid.validPercent(yAxis) * ySize
            xPnt = aecPoint(origin.x + (yAxis - (xWidth * 0.5)), origin.y)
            yPnt = aecPoint(origin.x, origin.y + (xAxis - (yDepth * 0.5)))
            self.makeBox(xPnt, xWidth, ySize)
            points = self.__aecGeometry.getBoxPoints(yPnt, xSize, yDepth)
            self.add(points)
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False

    def makeCylinder(self, origin: aecPoint = aecPoint(0, 0, 0), radius = 1) -> bool:

        """
        Contructs the perimeter as an approximate circle, setting 
        a ratio from the delivered radius to the number of sides.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if radius < 3: sides = 3
            else: sides = radius
            return self.makePolygon(origin, radius, sides)
        except Exception:
            traceback.print_exc()
            return False

    def makeH(self, origin: aecPoint = aecPoint(0, 0, 0),
                    xSize: float = 1, ySize: float = 1,
                    xWidth1 = 0.33333333, xWidth2= 0.33333333, yDepth = 0.33333333) -> bool:
        """
        Constructs an H-shaped boundary within the box defined by point and xy deltas.
        xWidth1, xWidth2, and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of each vertical and cross bar, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if self.makeCross(origin, xSize, ySize, xWidth1, yDepth, yAxis = (xWidth1 * 0.5)):
                xPoint = aecPoint(origin.x + (xSize - xWidth2), origin.y)
                points = \
                self.__aecGeometry.getBoxPoints(xPoint, xWidth2 * xSize, ySize)
                self.add(points)
                return self.__boundarySet
            return False
        except Exception:
            traceback.print_exc()
            return False

    def makeL(self, origin: aecPoint = aecPoint(0, 0, 0), 
                    xSize: float = 1, ySize: float = 1,
                    xWidth = 0.33333333, yDepth = 0.33333333) -> bool:
        """
        Constructs a L-shaped boundary within the box defined by point and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances
        that determine the width of each bar.
        Returns True on success.
        Returns False on failure.
        """
        try:
            return self.makeCross(origin, xSize, ySize, xWidth, yDepth, xWidth * 0.5, yDepth * 0.5)
        except Exception:
            traceback.print_exc()
            return False

    def makePolygon(self, origin: aecPoint = aecPoint(0, 0, 0), radius = 1, sides = 3) -> bool:
        """
        Constructs the boundary as a regular polygon centered on the delivered
        origin point with the first vertex at the maximum y-coordinate.
        Returns True on success.
        Returns False on failure.
        """
        try:
            radius = abs(radius)
            if radius == 0: return False
            sides = int(abs(sides))
            if sides < 3: sides = 3
            angle = math.pi * 0.5
            incAngle = (math.pi * 2) / sides
            points = []
            count = 0
            while count < sides:
                x = origin.x + (radius * math.cos(angle))
                y = origin.y + (radius * math.sin(angle))
                points.append(aecPoint(x, y))
                angle += incAngle
                count += 1
            return self.__setBoundary(points)
        except Exception:
            traceback.print_exc()
            return False
 
    def makeT(self, origin = aecPoint(0, 0, 0), 
                    xSize: float = 1, ySize: float = 1,
                    xWidth = 0.33333333, yDepth = 0.33333333) -> bool:
        """
        Constructs a T-shaped boundary within the box defined by point and xy deltas.
        xWidth and yDepth are percentages of overall x-axis and y-axis distances that
        determine the width of the vertical and horizonatl bars, respectively.
        Returns True on success.
        Returns False on failure.
        """
        try:
            return self.makeCross(origin, xSize, ySize, xWidth, yDepth, xAxis = (1 - (yDepth * 0.5)))
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
            if self.makeL(origin, xSize, ySize, xWidth1, yDepth):
                xWidth = xWidth2 * xSize
                xPoint = aecPoint(origin.x + (xSize - xWidth), origin.y)
                points = self.__aecGeometry.getBoxPoints(xPoint, xWidth, ySize)
                self.add(points)
                return self.__boundarySet
            return False
        except Exception:
            traceback.print_exc()
            return False        
    
    def mirror(self, points: List[aecPoint] = None) -> bool:
        """
        Mirrors the space orthogonally around the specified line as defined
        by two points, or by default around the major orthogonal axis.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if not points: points = self.axis_major
            newPoints = self.__aecGeometry.mirrorPoints2D(self.points, points[0], points[1])
            if not newPoints: return False
            self.__setBoundary(newPoints)
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False

    def moveBy(self, x: float = 0, y: float = 0, z: float = 0) -> bool:
        """
        Moves the boundary by the delivered x, y, and z displacements.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = [aecPoint(pnt.x + x, pnt.y + y) for pnt in self.points_floor]
            self.level += z
            return self.__setBoundary(points)
        except Exception:
            traceback.print_exc()
            return False

    def moveTo(self, fromPnt: aecPoint, toPnt: aecPoint) -> bool:
        """
        Attempts to move the boundary by constructing a vector between the "from" and "to" points.
        Returns True on success.
        Returns False on failure.
        """
        try:
            x = toPnt.x - fromPnt.x
            y = toPnt.y - fromPnt.y
            z = toPnt.z - fromPnt.z
            return self.moveBy(x, y, z)
        except Exception:
            traceback.print_exc()
            return False            

    def pointWithin(self) -> aecPoint:
        """
        Returns a random point within the boundary.
        Returns None if no point can be found or on failure.
        """
        try:
            box_pnts = self.points_box
            lowX = box_pnts.SW.x
            uppX = box_pnts.SE.x
            lowY = box_pnts.SW.y
            uppY = box_pnts.NW.y
            inPoint = False
            while not inPoint:
                xCoord = uniform(lowX, uppX)
                yCoord = uniform(lowY, uppY)
                inPoint = self.polygon.contains(shapely.Point(xCoord, yCoord))
            return aecPoint(xCoord, yCoord)
        except Exception:
            traceback.print_exc()
            return None

    def rotate(self, angle: float = 180, pivot: aecPoint = None) -> bool:
        """
        Rotates the space counterclockwise around the 2D pivot point
        by the delivered rotation in degrees.
        If no pivot point is provided, the space will rotate around its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            angle = float(angle)
            if not pivot: 
                centroid = self.centroid_floor
                pivot = (centroid.x, centroid.y)
            polygon = shapelyAffine.rotate(self.__polygon, angle, pivot)
            if type(polygon) != shapely.polygon.Polygon: return False
            self.__polygon = polygon
            points = [aecPoint(pnt[0], pnt[1]) for pnt in polygon.exterior.coords[:-1]]
            return self.__setBoundary(points)
        except Exception:
            traceback.print_exc()
            return False    
      
    def scale(self, x: float = 1, y: float = 1, z: float = 1, point: aecPoint = None) -> bool:
        """
        Scales the boundary by a vector from the delivered point.
        If no point is provided, the boundary will scale from its centroid.
        Returns True on success.
        Returns False on failure.
        """
        try:
            points = self.points_floor
            if not point:
                centroid = self.centroid
                point = (centroid.x, centroid.y)   
            polygon = shapelyAffine.scale(self.polygon, x, y, 1, point)
            if type(polygon) != shapely.polygon.Polygon: return False
            points = [aecPoint(pnt[0], pnt[1]) for pnt in polygon.exterior.coords[:-1]] 
            self.height *= float(z)
            return self.__setBoundary(points)
        except Exception:
            self.__setBoundary(points)
            traceback.print_exc()
            return False        
        
    def wrap(self, points: List[aecPoint]) -> bool:
        """
        Sets the boundary to a convex hull
        derived from the delivered list of points.
        Returns True if successful.
        Returns False on failure.
        """
        try:
            conHull = self.__aecGeometry.getConvexHull(points)
            if conHull: self.__setBoundary(conHull)
            return self.__boundarySet
        except Exception:
            traceback.print_exc()
            return False       
        
        