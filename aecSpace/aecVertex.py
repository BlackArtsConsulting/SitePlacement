import math
from numpy import array
import traceback
from typing import Tuple
from uuid import uuid4

from .aecGeometry import aecGeometry
from .aecPoint import aecPoint

class aecVertex():
    """
    Represents 2D or 3D Cartesian coordinates as well as data
    supporting participation in the definition of a boundary.
    """    
    
    __slots__ = \
    [
        '__angle_exterior',
        '__angle_interior',
        '__convex',
        '__ID',
        '__normal',
        '__point',
        '__pointNxt',
        '__pointNrm',
        '__pointPre'        
    ]
    
    __aecGeometry = aecGeometry()
      
    def __init__(self, pnt: aecPoint, pntPre: aecPoint, pntNrm: aecPoint, pntNxt: aecPoint):
        """
        Constructor records the vertex point and three adjacent points 
        to calculate angles, convexity, and point normal of the vertex.
        """   
        self.__ID = str(uuid4()) 
        self.__point = aecPoint(pnt.x, pnt.y, pnt.z)
        self.__pointPre = aecPoint(pntPre.x, pntPre.y, pntPre.z)
        self.__pointNrm = aecPoint(pntNrm.x, pntNrm.y, pntNrm.z)
        self.__pointNxt = aecPoint(pntNxt.x, pntNxt.y, pntNxt.z)
        angles = self.__aecGeometry.getAngles(self.__point, self.__pointPre, self.__pointNxt)
        self.__angle_exterior = angles.exterior
        self.__angle_interior = angles.interior
        self.__convex = angles.convex        
        preVector = self.__pointPre.xyz_array - self.__point.xyz_array
        nxtVector = self.__pointNxt.xyz_array - self.__point.xyz_array
        nrmVector = self.__pointNrm.xyz_array - self.__point.xyz_array
        normal = preVector + nxtVector + nrmVector
        if self.convex: normal *= -1
        self.__normal = tuple([1 if n > 0 else -1 if n < 0 else 0 for n in list(normal)])

    @property
    def angle_exterior(self) -> float:
        """
        Returns the angle at the exterior of the boundary at the vertex in radians.
        """
        try:
            return self.__angle_exterior
        except:
            traceback.print_exc()
            return None   
 
    @property
    def angle_exteriorD(self) -> float:
        """
        Returns the angle at the exterior of the boundary at the vertex in degrees.
        """
        try:
            return self.__angle_exterior * (180 / math.pi)
        except:
            traceback.print_exc()
            return None                

    @property
    def angle_interior(self) -> float:
        """
        Returns the angle at the interior of the boundary at the vertex in radians.
        """
        try:
            return self.__angle_interior
        except:
            traceback.print_exc()
            return None    
 
    @property
    def angle_interiorD(self) -> float:
        """
        Returns the angle at the interior of the boundary at the vertex in degrees.
        """
        try:
            return self.__angle_interior * (180 / math.pi)
        except:
            traceback.print_exc()
            return None   
    
    @property
    def convex(self) -> bool:
        """
        Property
        Indicates if the vertex is convex relative to the boundary interior.
        """
        try:
            return self.__convex
        except:
            traceback.print_exc()
            return None 

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
    def normal(self) -> Tuple[float, float, float]:
        """
        Property
        Returns the point normal of the vertex.
        """
        try:
            return self.__normal
        except:
            traceback.print_exc()
            return None 
        
    @property
    def normal_array(self) -> array:
        """
        Property
        Returns the point normal of the vertex.
        """
        try:
            return array(self.normal)
        except:
            traceback.print_exc()
            return None         
 
    @property
    def point(self) -> aecPoint:
        """
        Property
        Returns the point normal of the vertex.
        """
        try:
            return self.__point
        except:
            traceback.print_exc()
            return None 
        
    @property
    def xy(self) -> Tuple[float, float]:
        """
        Property
        Returns the point.
        """
        try:
            return self.__point.xy
        except Exception:
            traceback.print_exc()
            return None       
    
    @property
    def xyz(self) -> Tuple[float, float, float]:
        """
        Property
        Returns the point.
        """
        try:
            return self.__point.xyz
        except Exception:
            traceback.print_exc()
            return None   
                    