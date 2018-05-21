import random
import traceback

from shapely import geometry as shapely

from .aecCompass import aecCompass
from .aecGeomCalc import aecGeomCalc
from .aecSpace import aecSpace
from .aecErrorCheck import aecErrorCheck

"""
class aecSpacer
Provides calculation, positioning, and deployment
functions for multiple aecSpace objects.
"""
class aecSpacer:

    # utility objects and data shared by all instances.

    __aecErrorCheck = aecErrorCheck() # An instance of aecErrorCheck
    __aecGeomCalc = aecGeomCalc()     # An instance of aecGeomCalc
    __type = 'aecSpacer'              # Type identifier of object instances

    def __init__(self):
        """
        aecSpacer Constructor
        """
        pass

    def copy(self, space, moveBy = (0, 0, 0)):
        """
        aecSpace copy(aecSpace, (3D vector))
        Returns a new aecSpace that is a copy of the delivered aecSpace.
        The copy will be moved by the delivered vector.
        Returns None on failure.
        """
        try:
            if space.getType() != 'aecSpace': return None
            moveBy = self.__aecErrorCheck.checkPoint(moveBy)
            spcProp = space.getProperties()
            newSpace = aecSpace()
            for key in spcProp.keys():
                newSpace.setProperty(key, spcProp[key])
            if moveBy: newSpace.move(moveBy)
            return newSpace
        except Exception:
            traceback.print_exc() 
            return None

    def getType(self):
        """
        string getType()
        Returns a string constant to identify the object type.
        Returns None on failure.
        """
        try:
            return self.__type
        except Exception:
            traceback.print_exc()
            return None

    def place(self, space, copies = 1, moveBy = (0, 0, 0)):
        """
        [aecSpace,] place(aecSpace, int, (3D vector))
        Creates and returns a list of aecSpaces placed along a delivered vector.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            if space.getType() != 'aecSpace': return None
            moveBy = self.__aecErrorCheck.checkPoint(moveBy)
            if not moveBy: return None            
            spaces = []
            x = 0
            while x < copies:
                newSpace = self.copy(space, moveBy)
                spaces.append(newSpace)
                space = newSpace
                x += 1
            return spaces
        except Exception:
            traceback.print_exc()
            return None

    def placeWithin(self, shape, bound):
        """
        bool placeWithin(aecSpace, aecSpace, compassPoint)
        Attempts to place one aecSpace (shape) within the boundary 
        of another (bound) at a random interior point.
        Returns True on success.
        Returns False on failure.
        """
        try:
            if bound.getType() != 'aecSpace' or shape.getType() != 'aecSpace': return False
            if shape.getArea() > bound.getArea(): return False
            tstShape = self.copy(shape)
            level = bound.getLevel()
            bbox = bound.getBoundingBox()
            boxX = [int(x[0]) for x in bbox]
            boxY = [int(y[1]) for y in bbox]
            boxX.sort()
            boxY.sort()            
            within = False
            x = 0
            while not within and x < 100:
                xCoord = random.randint(boxX[0], boxX[-1])
                yCoord = random.randint(boxY[0], boxY[-1])
                bndPnt = (xCoord, yCoord, level)
                tstShape.moveTo(tstShape.getCentroid(), bndPnt)
                within = tstShape.getBoundary().within(bound.getBoundary())
                x += 1
            if not within: return False
            shape.moveTo(shape.getCentroid(), bndPnt)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def placeWithinLine(self, shape, bound, compass = aecCompass.N):
        """
        bool placeWithinLine(aecSpace, aecSpace, (3D point), (3D point))
        Attempts to place one aecSpace (shape) within the boundary of
        another (bound) at a random interior point along a specified line
        from the center of the boundary to the specified compass point on
        the boundary.
        Returns True on success.
        Returns False on failure.        
        """
        try:
            if bound.getType() != 'aecSpace' or shape.getType() != 'aecSpace': return False
            if shape.getArea() > bound.getArea(): return False
            tstShape = self.copy(shape)
            bndPnt = bound.getCompassPoint(orient = compass, point2D = True)
            level = bound.getLevel()
            within = False
            x = 0
            while not within and x < 100:
                vector = shapely.LineString([bound.getCentroid(point2D = True), bndPnt])
                posit = self.__aecErrorCheck.checkPercentage(random.randint(0, 100))
                point = vector.interpolate(posit, normalized = True)
                point = (point.x, point.y, level)
                tstShape.moveTo(tstShape.getCentroid(), point)
                within = tstShape.getBoundary().within(bound.getBoundary())
                x += 1
            if not within: return False
            shape.moveTo(shape.getCentroid(), point)
            return True
        except Exception:
            traceback.print_exc()
            return False        


    def row(self, space, copies = 1, gap = 0, xAxis = True):
        """
        [aecSpace,] row(aecSpace, int, number, bool)
        Creates and returns a list of aecSpaces placed along the x-axis from the delivered
        aecSpace by the bounding box width plus the distance added by the gap parameter.
        By default places new spaces along the positive x-axis from the position of the
        delivered aecSpace, or if xAxis is false, along the positive y-axis.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            if space.getType() != 'aecSpace': return None
            if xAxis:
                posBy = space.getXsize() + gap
                moveBy = (posBy, 0, 0)
            else:
                posBy = space.getYsize() + gap
                moveBy = (0, posBy, 0)
            return self.place(space, copies, moveBy)
        except Exception:
            traceback.print_exc()
            return None

    def stack(self, space, copies = 1, plenum = 0):
        """
        [aecSpace,] stacker(aecSpace, int, number)
        Creates and returns a list of aecSpaces stacked upward from the
        delivered aecSpace by the height of the aecSpace plus additional
        elevation added by the plenum parameter.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            if space.getType() != 'aecSpace': return None
            stackBy = space.getHeight() + plenum
            spaces = self.place(space, copies, (0, 0, stackBy))
            return spaces
        except Exception:
            traceback.print_exc()
            return None

    def stackToArea(self, space, area, plenum = 0):
        """
        [aecSpace,] buildToArea(aecSpace, number, number)
        Compares the area of the delivered aecSpace to the target area and stacks
        identical spaces from the original space until the target area is met or
        exceeded, returning a list of resulting aecSpaces.
        Returned list does not include the delivered aecSpace.
        Returns None on failure.
        """
        try:
            spcArea = space.getArea()
            if spcArea >= area: return []
            copies = int(area / spcArea)
            return self.stack(space, copies, plenum)
        except Exception:
            traceback.print_exc()
            return None

# end class
