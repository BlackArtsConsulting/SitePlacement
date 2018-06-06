import math
from numpy import array, cross
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
        '__point'
    ]
    
    __aecGeometry = aecGeometry()
      
    def __init__(self, pnt: aecPoint, pntPre: aecPoint, pntNxt: aecPoint):
        """
        Constructor records the vertex point and three adjacent points 
        to calculate angles, convexity, and point normal of the vertex.
        """   
        self.__ID = str(uuid4()) 
        self.__point = pnt
        angles = self.__aecGeometry.getAngles(pnt, pntPre, pntNxt)
        self.__angle_exterior = angles.exterior
        self.__angle_interior = angles.interior
        self.__convex = angles.convex        
        preVector = pntPre.xyz_array - pnt.xyz_array
        nxtVector = pntNxt.xyz_array - pnt.xyz_array
        preNormal = cross(preVector, nxtVector)
        normal = preNormal / (math.sqrt(sum(preNormal**2)))
        self.__normal = tuple(normal)

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
                    