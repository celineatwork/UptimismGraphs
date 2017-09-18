import struct
import uptimism.graph_object

class DataPoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinate = None
    
    def to_coordinate(self, xMin, xMax, yMin, yMax, negX, negY):
        cx = graph_math.normalise(self.x, xMin, xMax)
        cy = graph_math.normalise(self.y, yMin, yMax)
        
        if negY:
            cy = cy * -1

        if negX:
            cx = cx * -1

        self.coordinate = Coordinate(cx, cy)
        return self.coordinate
    
    @property
    def point(self):
        return (self.x, self.y)
    
    @property
    def coordinate(self):
        return self.coordinate

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y