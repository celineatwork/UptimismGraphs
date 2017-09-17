import cairo, cairograph, graph_math

class DataSet():
    def __init__(self, name):
        self.name = name
        self.rawData = []
        self.normalised = []
        self.yMin = None
        self.yMax = None
        self.xMin = None
        self.xMax = None
    
    def add(self, x, y):
        self.rawData.append(Coordinate(x, y))

        if x < self.xMin or self.xMin is None:
            self.xMin = x
        if x > self.xMax or self.xMax is None:
            self.xMax = x 

        if y < self.yMin or self.yMin is None:
            self.yMin = y
        if y > self.yMax or self.yMax is None:
            self.yMax = y
    
    def normaliseX(self):
        # sort by x (time) values then normalize x values
        self.rawData.sort(key=lambda c: c.x)
        self.normalised = map(lambda c: normalise(c.x, self.xMin, self.xMax), self.rawData)    

    def get_points(self, time_points):
        draw_points = []
        i0, i1 = None, None
        x0, x1 = None, None

        # get idx points that lie before and after time point t
        for t in time_points:
            # print ""
            idx = 0
            while idx < len(self.normalised):
                x = self.normalised[idx]
                # print y
                if x <= t:
                    x0 = x
                    idx += 1
                if x >= t:
                    x1 = x
                    break
            
            i0, i1 = self.normalised.index(x0), self.normalised.index(x1)

            # points that lie before after time point t
            p0, p1 = self.rawData[i0], self.rawData[i1]
            
            # get interpolated points at time
            if i0 != i1:
                interpX = to_value(normalise(t, x0, x1), p0.x, p1.x)
                interpY = get_y(interpX, p0, p1)
                # draw_points.append(Coordinate(p0.x, p0.y))
            else:
                # avoid zero division/is on time point
                interpY = p1.y
                interpX = p1.x

            draw_points.append(Coordinate(interpX, interpY))
        return draw_points

    def print_coord(self):
        print [(d.x, d.y) for d in self.rawData]


class LineGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(LineGraph, self).__init__(data)
        self.dataSet = {}
        self.pointSet = {}
        self.yMin = None
        self.yMax = None
        self.xMin = 0.0
        self.xMax = 120.0
        self.initialize()
    
    def initialize(self):
        for e in self.data:
            # (time, value)
            name, x, y = e["team"], float(e["ts"]), float(e["avg"])
            try:
                self.dataSet[name].add(x+120, y)
            except KeyError:
                self.dataSet[name] = DataSet(name)
                self.dataSet[name].add(x, y)
            
            # set global max/mins
            if x < self.xMin or self.xMin is None:
                self.xMin = x
            if x > self.xMax or self.xMax is None:
                self.xMax = x 

            if y < self.yMin or self.yMin is None:
                self.yMin = y
            if y > self.yMax or self.yMax is None:
                self.yMax = y
        
        self.set_surface_as_pattern(Colors.GRAY, 1024, 768)
        self.set_pen(0.005, Colors.BLACK)
        self.create()

    
    def create(self):
        # get frame times
        frames = 10
        time_points = self.get_ease_out_curve(frames)
        count = 0

        for team, data in self.dataSet.iteritems():
            data.normaliseX()
            self.pointSet[team] = data.get_points(time_points)
            count = len(self.pointSet[team])

        # for i in range(count):
        for i in range(count):
            for team, data in self.dataSet.iteritems():
                points = self.pointSet[team]

                c0 = cairograph.Coordinate(0.0, 0.0)
                c1 = points[i].to_ratio(
                    # self.xMin, self.xMax, self.yMin, self.yMax, False, True)
                    data.xMin, data.xMax, data.yMin, data.yMax, False, True)

                if i > 0:
                    c0 = points[i-1]

                self.ctx.move_to(c0.cx, c0.cy)
                self.create_frame()
                self.draw_line(c1.x,c1.y)
                print team, c0.x, c0.y
                print team, c1.x, c1.y
        
        # self.create_gif(frames/2)
                
        # for team, data in self.dataSet.iteritems():
        #     self.ctx.move_to(0.0, 0.0)
        #     for p in self.pointSet[team]:
        #         c = p.to_ratio(data.xMin, data.xMax, data.yMin, data.yMax, False, True)
        #         self.draw_line(c.x,c.y)
        #         print c.x, c.y
        #     self.create_frame()
        
def create(data):
    graph = LineGraph(data)