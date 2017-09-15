import cairo, cairograph, maththings, time

class LineGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(LineGraph, self).__init__(data)
        self.dataSet = {}
        self.pointSet = {}
        self.xMin = None
        self.xMax = None
        self.yMin = 0.0
        self.yMax = 120.0
        self.initialize()
    
    def initialize(self):
        # make grey background
        self.set_surface_as_pattern(1024, 768)

        for e in self.data:
            # (time, value)
            name, x, y = e["team"], float(e["ts"]), float(e["avg"])+120
            try:
                self.dataSet[name].add(x, y)
            except KeyError:
                self.dataSet[name] = DataSet(name)
                self.dataSet[name].add(x, y)
            
            # if x < self.xMin or self.xMin is None:
            #     self.xMin = x
            # if x > self.xMax or self.xMax is None:
            #     self.xMax = x 
        
        self.draw_v1()
            
    def draw_v1(self):
        self.set_pen(0.005, "")
        maxPoints = 0
        self.ctx.move_to(0.0, 0.0)

        for dataSet in self.dataSet.values():
            maxPoints = dataSet.length if dataSet.length > maxPoints else maxPoints
            dataSet.rawData.sort(key=lambda c: c.x)

        for i in range(maxPoints):
            for dataSet in self.dataSet.values():
                if i < dataSet.length:
                    coordinate = dataSet.get_coordinate(i, self.yMin, self.yMax)
                    self.ctx.move_to(dataSet.last.x, dataSet.last.y)
                    self.draw_line(coordinate.x, coordinate.y)
                    dataSet.last = coordinate
                    print coordinate.point
            self.create_frame()
            
                
                
            
            
            
        

class DataSet():
    def __init__(self, name):
        self.name = name
        self.rawData = []
        self.xMin = None
        self.xMax = None
        self.length = 0
        self.last = cairograph.Coordinate(0.0, 0.0)
    
    def add(self, x, y):
        self.rawData.append(cairograph.Coordinate(x, y))

        if x < self.xMin or self.xMin is None:
            self.xMin = x
        if x > self.xMax or self.xMax is None:
            self.xMax = x 
        
        self.length += 1
    
    def get_coordinate(self, idx, yMin, yMax):
        point = self.rawData[idx]
        coordinate = point.to_ratio(self.xMin, self.xMax, yMin, yMax, False, True)
        coordinate.y = coordinate.y * -1
        return coordinate