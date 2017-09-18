import cairo
from uptimism import graph_math
from uptimism.data_point import DataPoint
from uptimism.graph_object import GraphObject
from uptimism.colors import Colors

class DataSet():
    def __init__(self, team):
        self.team = team
        self.rawData = []
        self.points = []
        self.length = 0

    def add(self, x, y):
        self.rawData.append(DataPoint(x, y))
        self.length += 1

    def normaliseX(self, xMin, xMax):
        # sort by x (time) values then normalize x values
        self.rawData.sort(key=lambda dataPoint: dataPoint.x)
        return map(
            lambda dataPoint: graph_math.normalise(dataPoint.x, xMin, xMax), self.rawData)   
    
    def get_time_points(self, t_points, xMin, xMax, yMin, yMax):
        nPoints = self.normaliseX(xMin, xMax)
        print nPoints
        lower_idx = 0
        upper_idx = 0

        lower_x = nPoints[lower_idx]
        upper_x = nPoints[upper_idx]
        print "*", lower_x

        for t in t_points:
            print "t", t
            while lower_x <= t and lower_idx < self.length-1:
                lower_idx += 1
                lower_x = nPoints[lower_idx]
                print "lower_x", lower_x
            
            while upper_idx >= t and upper_idx < self.length-1:
                upper_idx += 1
                upper_x = nPoints[upper_idx]
            
            lower_idx -= 1
            upper_idx -= 1

            lower_x = nPoints[lower_idx]
            upper_x = nPoints[upper_idx]

            print round(lower_x, 4), round(t, 4), round(upper_x, 4)
            print ""
            

                    
                
    
    # def get_coordinate(self, idx, yMin, yMax):
    #     point = self.rawData[idx]
    #     coordinate = point.to_ratio(self.xMin, self.xMax, yMin, yMax, False, True)
    #     coordinate.y = coordinate.y * -1
    #     return coordinate


class LineGraph(GraphObject):
    def __init__(self, data):
        super(LineGraph, self).__init__(data)
        self.xMin = 0.0
        self.xMax = 0.0
        self.yMin = 0.0
        self.yMax = 120.0 # this is specified for decibels
        self.fCount = 20
        self.dataSets = self.process(data)
        self.initialize()
    
    def process(self, data):
        dataSets = {}
        for e in data:
            # (time, value)
            name, x, y = e["team"], float(e["ts"]), float(e["avg"]) + self.yMax
            
            try:
                dataSets[name].add(x, y)
            except KeyError:
                dataSets[name] = DataSet(name)
                dataSets[name].add(x, y)
            
            # get max/min x values (time)
            if x < self.xMin:
                self.xMin = x

            if x > self.xMax:
                self.xMax = x 
        
        return dataSets

    def initialize(self):
        # make grey background
        self.set_surface_as_pattern(Colors.GRAY, 1024, 768)
        self.set_pen(0.005, Colors.BLACK)

        self.create()

    def create(self):
        # calls to graph_object
        time_points = self.get_ease_out_curve(self.fCount)
        print self.dataSets
        for dataSet in self.dataSets.values():
            dataSet.get_time_points(time_points, self.xMin, self.xMax, self.yMin, self.yMax)
        