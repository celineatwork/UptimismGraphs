import cairo, imageio, cairograph, maththings

class LineGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(LineGraph, self).__init__(data)
        self.points = {}
        self.create()
    
    def create(self):
        # set bg
        bg = cairo.SolidPattern(1.0, 1.0, 1.0, 1.0)
        self.ctx.set_source (bg)
        self.ctx.fill ()

        self.draw_lines()

    def draw_lines(self):
        # set pen width
        self.ctx.set_line_width (0.005)
        
        # bottom left corner
        self.ctx.translate (0.0, 1.0)
        self.ctx.move_to (0, 0)

        self.normalize_scores()
        frames = 100 - self.data["pointCount"]
        curve_values = self.get_ease_out_curve(frames)
        idx = 0
        
        for c in curve_values:
            for k, v in self.dataset.iteritems():
                # raw tuples (x, y)
                points = v["points"]
                
                # normalised values
                xpoints = v["xpoints"]
                
                x2 = xpoints[idx]
                if c > x2:
                    idx += 1
                    self.points[k] += v["points"][idx]
                
                p1, p2 = points[idx], points[idx+1]
                x1, x2 = xpoints[idx], xpoints[idx+1]

                # calculate draw coordinates for interpolated point
                x_value = maththings.normalise(t, x1, x2)
                x = maththings.to_value(x_value, p1[0], p[1])
                y = maththings.get_y(x, p1, p2)
                

    

    def add_coordinate(self, team, team_data):
        self.dataset[team]
        
                
                
            
    
    def normalize_scores(self):
        for k, v in self.dataset.iteritems():
            self.points[k]["points"] = []
            self.dataset[k]["xpoints"] = [maththings.normalize(p[0], self.data["xMin"], self.data["xMax"]) for p in v["points"]]

def create(data):
    graph = LineGraph(data)