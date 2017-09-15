import cairo, cairograph, time

class BarGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(BarGraph, self).__init__(data)
        self.dataSet = {}
        self.yMax = 0
        self.initialize()
    
    def initialize(self):
        self.set_surface_as_pattern(768, 924)
        self.set_pen(0.005, "ffffff")

        for e in self.data:
            name, volume = e["team"], float(e["volume"])
            self.dataSet[name] = DataSet(name, volume)

            if volume > self.yMax:
                self.yMax = volume

        
        # width = 100
        # height = 100
        # self.ctx.move_to(0,0.5)
        # self.ctx.rel_line_to(width, 0)
        # self.ctx.rel_line_to(0, height)
        # self.ctx.rel_line_to(-width, 0)
        # self.ctx.close_path()
        # self.draw_line(0.1, 0.5)

        self.ctx.rotate(-0.45)
        
        # h = 1.0
        # y = 0.6 - h
        # print y
        # self.ctx.rectangle (0.3, y, 0.25, h)
        # self.ctx.fill()

        # h = 0.8
        # y = 0.6 - h
        # print y
        # self.ctx.rectangle (0.65, y, 0.25, h)
        # self.ctx.fill()

        # self.create_frame()

        t = time.time()
        time_points = self.get_ease_out_curve(60)
        for t in time_points:
            left = True
            for dataSet in self.dataSet.values():
                height = dataSet.volume / self.yMax * t
                self.draw_graph(left, height)
                left = False
            self.create_frame()
        t1 = time.time()
        print (t1 - t)

        # for dataSet in self.dataSet.values():
        # self.ctx.rectangle(0, 0.5, 100, 100)
                
        # self.create_frame()
        # self.create_gif(40)
    
    def draw_graph(self, left, height):
        y = 0.5 - height
        if left:
            self.ctx.rectangle (0.3, y, 0.25, height)
        else:
            self.ctx.rectangle (0.65, y, 0.25, height)
        self.ctx.fill()
            


class DataSet():
    def __init__(self, team, volume):
        self.team = team
        self.volume = volume
    