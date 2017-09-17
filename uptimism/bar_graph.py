import cairo, cairograph
from colors import Colors

class DataSet():
    def __init__(self, team, volume):
        self.team = team
        self.volume = volume


class BarGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(BarGraph, self).__init__(data)
        self.dataSet = {}
        self.yMax = 0
        self.initialize()
    
    def initialize(self):
        self.set_surface_as_pattern(Colors.GRAY, 768, 924)
        self.set_pen(0.005, Colors.BLACK)

        for e in self.data:
            name, volume = e["team"], float(e["volume"])
            self.dataSet[name] = DataSet(name, volume)

            if volume > self.yMax:
                self.yMax = volume

        self.create()
    
    def create(self):
        self.ctx.rotate(-0.45)

        # calls to graph_object
        time_points = self.get_ease_out_curve(60)
        
        # makes series of frames for bar graphs growing
        for t in time_points:
            left = True
            for dataSet in self.dataSet.values():
                height = dataSet.volume / self.yMax * t
                self.draw_graph(left, height)
                left = False
            self.create_frame()
    
    def draw_graph(self, left, height):
        y = 0.5 - height
        if left:
            self.ctx.rectangle (0.3, y, 0.25, height)
        else:
            self.ctx.rectangle (0.65, y, 0.25, height)
        self.ctx.fill()
    