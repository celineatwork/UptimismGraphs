import cairo, cairograph

class BarGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(BarGraph, self).__init__(data)
        self.dataSet = {}
        # self.pointSet = {}
        # self.yMin = None
        # self.yMax = None
        # self.xMin = None
        # self.xMax = None
        self.process()
    
    def process(self):
        for e in self.data:
            # (time, value)
            name, x, y = e["team"], float(e["ts"]), float(e["avg"])
            try:
                self.dataSet[name].add(x, y)
            except KeyError:
                self.dataSet[name] = cairograph.DataSet(name)
                self.dataSet[name].add(x, y)
            