import cairo, imageio, cairograph, maththings, time

class LineGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(LineGraph, self).__init__(data)
        self.dataSet = {}
        self.pointSet = {}
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
        self.do_things()
    
    def do_things(self):
        # get frame times
        frames = 10
        time_points = self.get_ease_out_curve(frames)
        # count = 0

        for team, data in self.dataSet.iteritems():
            data.normaliseX()
            self.pointSet[team] = data.get_points(time_points)
            # count = len(self.pointSet[team])
        
        # self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)

        # for i in range(count):
        for i in range(frames):
            for team, data in self.dataSet.iteritems():
                points = self.pointSet[team]

                c0 = cairograph.Coordinate(0.0, 0.0)
                c1 = points[i].to_ratio(
                    data.xMin, data.xMax, data.yMin, data.yMax, False, True)

                if i > 0:
                    c0 = points[i-1]

                self.ctx.move_to(c0.cx, c0.cy)
                self.create_frame()
                self.draw_line(c1.x,c1.y)
                
        # for team, data in self.dataSet.iteritems():
        #     self.ctx.move_to(0.0, 0.0)
        #     for p in self.pointSet[team]:
        #         c = p.to_ratio(data.xMin, data.xMax, data.yMin, data.yMax, False, True)
        #         self.draw_line(c.x,c.y)
        #         print c.x, c.y
        #     self.create_frame()
        

def create(data):
    graph = LineGraph(data)