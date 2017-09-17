import graph_math

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cx = 0.0
        self.cy = 0.0
    
    def to_ratio(self, xMin, xMax, yMin, yMax, negX, negY):
        # why am I doing double assigning? :/
        self.cx = graph_math.normalise(self.x, xMin, xMax)
        self.cy = graph_math.normalise(self.y, yMin, yMax)
        return Coordinate(self.cx, self.cy)
    
    @property
    def point(self):
        return (self.x, self.y)
    
    @proprty
    def coordinate(self):
        return Coordinate(self.cx, self.cy)