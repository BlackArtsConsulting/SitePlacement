import math
import numpy
import traceback
import uuid

from shapely import geometry as shapely
from .aecDataTypes import Coord3D
from .aecGeomCalc import aecGeomCalc


class aecVertex():
    """
    Represents 2D or 3D Cartesian coordinates as well as data
    supporting participation in the definition of a boundary.
    """
    __slots__ = \
    [
        '__angleExterior', 
        '__angleInterior',
        '__convex'
        '__identifier', 
        '__point'        
        '__x', 
        '__y', 
        '__z', 
    ]
    __aecGeomCalc = aecGeomCalc()      # An instance of aecGeomCalc    
      
    def __init__(self, x:float = 0, y:float = 0, z:float = 0):
        """
        aecPoint constructor defaults to origin point coordinates.
        """
        self.__angleExterior = 0.0
        self.__angleInterior = 0.0
        self.__convex = True
        self.__identifier = uuid.uuid4()
        self.__point = Coord3D(x = x, y = y, z = z)        
        self.__x = float(x)
        self.__y = float(y)
        self.__z = float(z)

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

    @property
    def ID(self) -> str:
        """
        Property
        Returns the UUID.
        """            
        try:
            return self.__identifier
        except Exception:
            traceback.print_exc()
            return None
        
    @property
    def x(self) -> float:
        """
        Property
        Returns the x coordinate.
        """          
        try:
            return self.__x
        except Exception:
            traceback.print_exc()
            return None    
    
    @x.setter
    def x(self, x:float = 0) -> bool:
        """
        Property
        Sets the x coordinate.
        Returns True on success.
        Returns False on failure.                
        """                  
        try:
            self.__x = float(x)
            return True
        except Exception:
            traceback.print_exc()
            return False          
       
    @property
    def y(self) -> float:
        """
        Property
        Returns the y coordinate.
        """                 
        try:
            return self.__y
        except Exception:
            traceback.print_exc()
            return None    
    
    @y.setter
    def y(self, y:float = 0) -> bool:
        """
        Property
        Sets the y coordinate.
        Returns True on success.
        Returns False on failure.        
        """              
        try:
            self.__y = float(y)
            return True
        except Exception:
            traceback.print_exc()
            return False
    
    @property
    def z(self) -> float:
        """
        Property
        Returns the z coordinate.
        """            
        try:
            return self.__z
        except Exception:
            traceback.print_exc()
            return None    
    
    @z.setter
    def z(self, z:float = 0) -> bool:
        """
        Property
        Sets the z coordinate.
        Returns True on success.
        Returns False on failure.        
        """           
        try:
            self.__z = float(z)
            return True
        except Exception:
            traceback.print_exc()
            return False

    @property
    def xy(self) -> Coord2D:
        """
        Property
        Returns the x and y coordinates as a namedtuple.
        Use .x and .y to access each coordinate from the result.
        """         
        try:
            return Coord2D._make([self.__x, self.__y])
        except Exception:
            traceback.print_exc()
            return None  
         
    @xy.setter
    def xy(self, coord: Coord2D) -> bool:
        """
        Property
        Sets the x and y coordinates.
        Returns True on success.
        Returns False on failure and reverts coordinate values.      
        """         
        try:
            x = self.__x
            y = self.__y 
            self.__x = float(coord.x)
            self.__y = float(coord.y)
            return True
        except Exception:
            self.__x = x
            self.__y = y             
            traceback.print_exc()
            return False
        
    @xy.setter
    def xy(self, coord: tuple) -> bool:
        """
        Property
        Sets the x and y coordinates.
        Returns True on success.
        Returns False on failure and reverts coordinate values.
        """         
        try:
            x = self.__x
            y = self.__y 
            self.__x = float(coord[0])
            self.__y = float(coord[1])
            return True
        except Exception:
            self.__x = x
            self.__y = y             
            traceback.print_exc()
            return False        
                   
    @property
    def xyz(self) -> Coord3D:
        """
        Property
        xyz returns the coordinates as a Coord3D namedtuple.
        Use .x, .y, and .z to access each coordinate from the result.
        """
        try:
            return Coord3D._make([self.__x, self.__y, self.__z])
        except Exception:
            traceback.print_exc()
            return None           
    
    @xyz.setter
    def xyz(self, coord: Coord3D) -> bool:
        """
        Property
        coord3D(Coord3D) sets the coordinates.
        Returns True on success.
        Returns False on failure and reverts coordinate values.      
        """
        try:
            x = self.__x
            y = self.__y
            z = self.__z
            self.__x = float(coord.x)
            self.__y = float(coord.y)
            self.__z = float(coord.z)
            return True
        except Exception:
            self.__x = x
            self.__y = y             
            self.__z = z
            traceback.print_exc()
            return False

    @xyz.setter
    def xyz(self, coord: tuple) -> bool:
        """
        Property
        Sets the x and y coordinates.
        Returns True on success.
        Returns False on failure and reverts coordinate values.      
        """         
        try:
            x = self.__x
            y = self.__y
            z = self.__z
            self.__x = float(coord[0])
            self.__y = float(coord[1])
            self.__z = float(coord[2])
            return True
        except Exception:
            self.__x = x
            self.__y = y  
            self.__z = z              
            traceback.print_exc()
            return False  

    @property
    def xy_array(self):
        """
        Property
        Returns the 2D coordinates as a numpy array.
        """
        try:
            return numpy.array([self.__x, self.__y])
        except Exception:
            traceback.print_exc()
            return None   

    @property
    def xy_list(self):
        """
        Property
        Returns the 2D coordinates as a list.
        """
        try:
            return [self.__x, self.__y]
        except Exception:
            traceback.print_exc()
            return None 

    @property
    def xy_shapely(self)-> shapely.Point:
        """
        Property
        Returns the 2D coordinates as a Shapely 2D point.
        """
        try:
            return shapely.Point([self.__x, self.__y])
        except Exception:
            traceback.print_exc()
            return None 

    @property
    def xy_tuple(self) -> tuple:
        """
        Property
        Returns the 2D coordinates as a tuple.
        """
        try:
            return (self.__x, self.__y)
        except Exception:
            traceback.print_exc()
            return None 

    @property
    def xyz_array(self):
        """
        Property
        Returns the 3D coordinates as a numpy array.
        """
        try:
            return numpy.array([self.__x, self.__y, self.__z])
        except Exception:
            traceback.print_exc()
            return None    

    @property
    def xyz_list(self):
        """
        Property
        Returns the 3D coordinates as a list.
        """
        try:
            return [self.__x, self.__y, self.__z]
        except Exception:
            traceback.print_exc()
            return None       

    @property
    def xyz_tuple(self):
        """
        Property
        Returns the 3D coordinates as a tuple.
        """
        try:
            return (self.__x, self.__y, self.__z)
        except Exception:
            traceback.print_exc()
            return None        
                 
    def moveBy(self, x:float = 0, y:float = 0, z:float = 0):
        """
        Changes each coordinate by the corresponding delivered value.
        Return True on success.
        Returns False on failure and reverts coordinate values.         
        """
        try:
            x = self.__x
            y = self.__y
            z = self.__z                    
            self.__x += float(x)
            self.__y += float(y)
            self.__z += float(z)
            return True
        except Exception:
            self.__x = x
            self.__y = y             
            self.__z = z             
            traceback.print_exc()
            return False
    
    def setAngles(self, prvPoint: aecVertex, nxtPoint: aecVertex,) -> bool:
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
    
                    