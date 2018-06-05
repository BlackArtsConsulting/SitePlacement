import math
import traceback

from .aecErrorCheck import aecErrorCheck
from .aecGeomCalc import aecGeomCalc
from .aecPoint2D import aecPoint2D

class aecVertex2D(aecPoint2D):
    """
    class aecVertex2D
    Defines a 3D vertex as a component of an aecBoundary.
    The XY plane is considered horizontal, the Z dimension vertical.
    """
    
    # utility objects and data shared by all instances.

    __aecErrorCheck = aecErrorCheck()  # An instance of aecErrorCheck
    __aecGeomCalc = aecGeomCalc()      # An instance of aecGeomCalc
        
    def __init__(self, points, index: int):
        """
        aecPoint Constructor
        Sets the ID to a new UUID.
        Creates a new aecErrorCheck object.
        if point coordinates are delivered, checks and uses them,
        otherwise sets the coordinates to the origin.
        """
        self.__angleExterior = None    # Angle in radians at the exterior of the vertex 
        self.__angleInterior = None    # Angle in radians at the interior of the vertex  
        self.__convex = None           # Boolean storing state of angle at vertex
        self.setVertex(points, index)
                 
    @property
    def angleExterior(self) -> float:
        """
        float angleExterior()
        Returns the angle at the exterior of the boundary at the vertex in radians.
        """
        try:
            return self.__angleExterior
        except:
            traceback.print_exc()
            return None   
 
    @property
    def angleExteriorD(self) -> float:
        """
        float angleExteriorD()
        Returns the angle at the exterior of the boundary at the vertex in degrees.
        """
        try:
            return self.__angleExterior * (180 / math.pi)
        except:
            traceback.print_exc()
            return None                

    @property
    def angleInterior(self) -> float:
        """
        float angleInterior()
        Returns the angle at the interior of the boundary at the vertex in radians.
        """
        try:
            return self.__angleInterior
        except:
            traceback.print_exc()
            return None    
 
    @property
    def angleInteriorD(self) -> float:
        """
        float angleInteriorD()
        Returns the angle at the interior of the boundary at the vertex in degrees.
        """
        try:
            return self.__angleInterior * (180 / math.pi)
        except:
            traceback.print_exc()
            return None   
    
    @property
    def convex(self) -> bool:
        """
        Indicates if the vertex is convex relative to the boundary interior.
        """
        try:
            return self.__convex
        except:
            traceback.print_exc()
            return None    
    
    def setVertex(self, points, index: int) -> bool:
        """
        Sets the vertex 3D point and angles.
        Returns True on success.
        Returns False on failure.
        """
        try:
            point = points[index]
            prvPoint = points[(index - 1) % len(points)]
            nxtPoint = points[(index + 1) % len(points)]
            angles = self.__aecGeomCalc.getAngles(point, prvPoint, nxtPoint)
            if not angles: return False
            self.__convex = angles.convex
            self.__angleExterior = angles.exterior
            self.__angleInterior = angles.interior
            self.__xyz = point.xyz
            return True
        except:
            traceback.print_exc() 
            return False

# end class
