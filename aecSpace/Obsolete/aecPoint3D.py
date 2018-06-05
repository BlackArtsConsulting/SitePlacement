import numpy
import traceback
import uuid

from .aecDataTypes import Coord3D
from .aecPoint2D import aecPoint2D

class aecPoint3D(aecPoint2D):
    """
    Represents 2D or 3D Cartesian coordinates.
    """
    __slots__ = ['__z']   
      
    def __init__(self, x:float = 0, y:float = 0, z:float = 0):
        """
        aecPoint constructor defaults to origin point coordinates.
        """
        super(aecPoint3D, self).__init__(x = x, y = y)
        self.__z = float(z)
        self.__identifier = uuid.uuid4()  
       
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
    
    
    
                    