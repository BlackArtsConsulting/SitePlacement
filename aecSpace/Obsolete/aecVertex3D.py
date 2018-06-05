import math
import numpy
import traceback
import uuid

from .aecErrorCheck import aecErrorCheck
from .aecGeomCalc import aecGeomCalc
from .aecPoint import aecPoint

class aecVertex(aecPoint):
    """
    class aecVertex
    Defines a 3D vertex as a component of the boundary of an aecSpace,
    with additional information for geometric and graphic calculations.
    The XY plane is considered horizontal, the Z dimension vertical.
    """
    
    # utility objects and data shared by all instances.

    __aecErrorCheck = aecErrorCheck() # An instance of aecErrorCheck
    __aecGeomCalc = aecGeomCalc()     # An instance of aecGeomCalc
        
    def __init__(self, points, index, nrmPoint):
        """
        aecPoint Constructor
        Sets the ID to a new UUID.
        Creates a new aecErrorCheck object.
        if point coordinates are delivered, checks and uses them,
        otherwise sets the coordinates to the origin.
        """
        self.__angleExterior = None             # Angle in radians at the exterior of the vertex 
        self.__angleInterior = None             # Angle in radians at the interior of the vertex  
        self.__convex = None                    # Boolean storing state of angle at vertex
        self.__normal = None                    # The normal vector of the vertex 
        self.__point = None                     # The x,y,z coordinates as a 3 digit tuple
        self.setVertex(points, index, nrmPoint)
                 
    @property
    def angleExterior(self):
        """
        float angleExterior()
        Returns the angle at the exterior of the polygon at the vertex in radians.
        """
        try:
            return self.__angleExterior
        except:
            traceback.print_exc()
            return None   
 
    @property
    def angleExteriorD(self):
        """
        float angleExteriorD()
        Returns the angle at the exterior of the polygon at the vertex in degrees.
        """
        try:
            return self.__angleExterior * (180 / math.pi)
        except:
            traceback.print_exc()
            return None                

    @property
    def angleInterior(self):
        """
        float angleInterior()
        Returns the angle at the interior of the polygon at the vertex in radians.
        """
        try:
            return self.__angleInterior
        except:
            traceback.print_exc()
            return None    
 
    @property
    def angleInteriorD(self):
        """
        float angleInteriorD()
        Returns the angle at the interior of the polygon at the vertex in degrees.
        """
        try:
            return self.__angleInterior * (180 / math.pi)
        except:
            traceback.print_exc()
            return None   

    @property       
    def normal(self):
        """
        (Coord3D) getNormal()
        Returns the point normal of the vertex.
        Returns None on failure.        
        """
        try:           
            return self.__normal
        except:
            traceback.print_exc()
            return None
    
               
    def __setNormal(self, point, prvPoint, nxtPoint, nrmPoint):
        """
        INTERNAL
        bool __setNormal((3D point), (3D point), (3D point), (3D point))
        Sets a point normal calculated from the delivered list
        of points asserted to be adjacent on a 3D polyhedron.
        Returns True on success.
        Returns False on failure.        
        """
        try:
            point = numpy.array(point)
            prvPoint = numpy.array(prvPoint)
            nxtPoint = numpy.array(nxtPoint)
            nrmPoint = numpy.array(nrmPoint)
            prvVector = prvPoint - point
            nxtVector = nxtPoint - point
            nrmVector = nrmPoint - point
            normal = prvVector + nxtVector + nrmVector
            if self.__angleInterior <= self.__angleExterior: normal *= -1
            normal = list(normal)   
            self.__normal = tuple([1 if n > 0 else -1 if n < 0 else 0 for n in normal])
            return True
        except:
            traceback.print_exc() 
            return False
 
    def setVertex(self, vtxBound, nrmBound, index):
        """
        bool setVertex(aecBoundary, aecBondary, int)
        Sets the vertex 3D point, angle, and point normal.
        Returns True on success.
        Returns False on failure.
        """
        try:
            point = vtxBoundary[index]
            prvPoint = points[(index - 1) % len(points)]
            nxtPoint = points[(index + 1) % len(points)]
            inVector = (point[0] - prvPoint[0], point[1] - prvPoint[1])
            outVector = (nxtPoint[0] - point[0], nxtPoint[1] - point[1])
            if numpy.cross(inVector, outVector) >= 0: self.__convex = True
            else: self.__convex = False
            cosAngle = numpy.dot(inVector, outVector)
            sinAngle = numpy.linalg.norm(numpy.cross(inVector, outVector))
            vtxAngle = numpy.arctan2(sinAngle, cosAngle)
            if self.__convex: self.__angleInterior = vtxAngle
            else: self.__angleInterior = (math.pi * 2) - vtxAngle
            self.__angleExterior = (math.pi * 2) - self.__angleInterior
            self.__setNormal(point, prvPoint, nxtPoint, nrmPoint)
            self.__point = point
            return True
        except:
            traceback.print_exc() 
            return False

# end class
