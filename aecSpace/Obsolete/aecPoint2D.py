import numpy
import traceback
import uuid

from shapely import geometry as shapely
from .aecDataTypes import Coord2D

class aecPoint2D():
    """
    Represents 2D Cartesian coordinates.
    """
    __slots__ = ['__x', '__y', '__identifier']   
      
    def __init__(self, x:float = 0, y:float = 0):
        """
        aecPoint constructor defaults to origin point coordinates.
        """
        self.__x = float(x)
        self.__y = float(y)
        self.__identifier = uuid.uuid4()  

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
          
    def moveBy(self, x:float = 0, y:float = 0, z:float = 0):
        """
        Changes each coordinate by the corresponding delivered value.
        Return True on success.
        Returns False on failure and reverts coordinate values.         
        """
        try:
            x = self.__x
            y = self.__y
            self.__x += float(x)
            self.__y += float(y)
            return True
        except Exception:
            self.__x = x
            self.__y = y             
            traceback.print_exc()
            return False
    
    
    
                    