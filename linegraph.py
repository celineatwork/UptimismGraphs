import cairo, imageio, cairograph, maththings, time

class LineGraph(cairograph.GraphObject):
    def __init__(self, data):
        super(LineGraph, self).__init__(data)
        self.dataSet = {}
        self.pointSet = {}
        self.process()
    
    def process(self):
        for e in self.data:
            name, x, y = e["team"], float(e["avg"]), float(e["ts"])
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
        
        # sort by y (time) values
        for team, data in self.dataSet.iteritems():
            self.ctx.move_to(0,0)
            data.normaliseY()
            self.pointSet[team] = data.get_points(time_points)
            for p in self.pointSet[team]:
                c = p.to_ratio(data.xMin, data.xMax, data.yMin, data.yMax)
                print (c.x,-c.y)
                self.draw_line(c.x,-c.y)
                self.create_frame()
            print ""


            

    # def process(self):
    #     count = 0
    #     for item in self.data:
    #         name, x, y = item["team"], float(item["avg"]), float(item["ts"])
    #         try:
    #             self.points[name]["data"].append((x, y))
    #         except KeyError:
    #             self.points[name] = {}
    #             self.points[name]["last"] = (0.0, 0.0)
    #             self.points[name]["data"] = [(x, y)]

            
            # used later for normalisation
            # if x < self.xmin:
            #     self.xmin = x
            # if x > self.xmax:
            #     self.xmax = x 

            # if y < self.ymin:
            #     self.ymin = y
            # if y > self.ymax:
            #     self.ymax = y
            # count += 1
        # print count
        
        # order by time/y axis
    #     self.points[name]["data"].sort(key=lambda tup: tup[1])
    #     self.normalize()
    
    # def normalize(self):
    #     frames = 10
    #     time_points = self.get_ease_out_curve(frames)
        # print time_points
        # sections = {}

        # for t in time_points:
        #     sections[t] = []
        
        # for name, v in self.points.iteritems():
        #     # v["data"] = map(lambda (x,y): (x, y, maththings.normalize(y, self.ymin, self.ymax)), v["data"])
        #     ymin = 
        #     v["yNorm"] = map(lambda (x,y): maththings.normalize(y, ymin, ymax), v["data"])
        #     print v["yNorm"]
        #     print ""
        
        # for i in range(frames):
        #     t1, t2, points = time_points[i], time_points[i+1], []
        #     for k, v in self.points.iteritems():
        #         idx, y1, y2 = 0, None, None
                
        #         while idx < len(v["data"])-1:
        #             y = v["yNorm"][idx]

        #             if y <= t1:
        #                 y1 = y
        #                 idx += 1
        #             else:
        #                 y2 = y

                        # p1, p2 = v["data"][idx], v["data"][idx+1]
                        # y1, y2 = v["yNorm"][idx], v["yNorm"][idx+1]
                        
                        # interpY = maththings.to_value(maththings.normalize(t2, y1, y2), p1[1], p2[1])
                        # interpX = maththings.get_x(interpY, p1, p2)
                        
                        # print interpY, interpX
                        # interpX = maththings.get_x(interpY, p1, p2)
                        # points.append( (interpX, interpY, k) )
                        # print (interpX, interpY)
                        
            #             break
            #     print y1, t1, y2
            
            # self.plot_points(points)
        # time.sleep(100)
    
    # def plot_points(self, draw_points):
    #     for p in draw_points:
    #         last = self.points[p[2]]["last"]
    #         x = maththings.normalize(p[0], self.xmin, self.xmax)
    #         y = maththings.normalize(p[1], self.ymin, self.ymax)
    #         self.ctx.move_to(last[0], last[1])
    #         self.draw_line(x, -y)
            
    #         self.points[p[2]]["last"] = (x, -y)
    #         # print p[2], x, -y
    #     self.create_frame()




            # (teamName, raw x, raw y, norm y)
            
    #         for i in range(frames):
    #             t1, t2 = time_points[i], time_points[i+1]
    #             sections[t2].extend(list(filter(lambda e: t1 <= e[3] <= t2, v["data"])))

    #     self.plot_points(time_points, sections)
        
    # def plot_points(self, time_points, sections):
    #     for t in time_points:
    #         s = sections[t]
    #         s.sort(key=lambda tup: tup[2])
            
    #         for e in s:
    #             p1, p2 
                
                
        


        # for k, v in self.points.iteritems():
        #     self.points[k]["xNormalized"] = []
        #     self.points[k]["coordinates"] = []
        #     # self.points[k]["count"] = -1
        #     # self.points[k]["idx"] = 0
            
        #     for p in v["raw"]:
        #         xNorm = maththings.normalize(p[0], self.xmin, self.xmax)
        #         self.points[k]["xNormalized"].append(xNorm)

        #         idx = 0
        #         t = time_points[idx]
        #         while idx < frames:
        #             t = time_points[idx]
        #             if xNorm > t:
        #                 sections[t].append( (k, xNorm, p[1]) )
        #                 break
        #             idx += 1
        
        # for k, v in sections.iteritems():
        #     print ""
        #     print k
        #     print v
                        
            
            #     self.points[k]["count"] += 1

            # if self.min_frames < self.points[k]["count"]:
            #     self.min_frames = self.points[k]["count"]

            # print k, self.points[k]["count"], [round(x, 2) for x in self.points[k]["xNormalized"]]
            # print ""
        # self.plot_points()
    
    # def plot_points(self):
    #     print ""
    #     # maybe do a thing for minimum frames
    #     frames = 100 - self.min_frames
    #     time_points = self.get_ease_out_curve(frames)
    #     sections = {}

    #     for t in time_points:
    #         sections[t] = []

        # for k, v in self.points.iteritems():
        #     for i in range(len(v["xNormalized"])):
        #         # iterate through and add to respective sections
        #         xNorm = v["xNormalized"][i]
        #         if tif xNorm <=




        # for i in range(frames):
        #     t = time_points[i]
        #     print "*", t
        #     for team in teams:
        #         print ""
        #         print team
        #         idx = self.points[team]["idx"]
        #         x1 = self.points[team]["xNormalized"][idx]

        #         while x1 <= t:
        #             x2 = self.points[team]["xNormalized"][idx+1]
        #             p1, p2 = self.points[team]["raw"][idx], self.points[team]["raw"][idx+1]
        #             xInterp = maththings.to_value(maththings.normalize(t, x1, x2), p1[0], p2[0])
                    
        #             self.points[team]["idx"] += 1
        #             x1 = self.points[team]["xNormalized"][idx]
                    
        #             print xInterp


                    
                






    
#     def create(self):
#         # set bg
#         bg = cairo.SolidPattern(1.0, 1.0, 1.0, 1.0)
#         self.ctx.set_source (bg)
#         self.ctx.fill ()

#         self.draw_lines()

#     def draw_lines(self):
#         # set pen width
#         self.ctx.set_line_width (0.005)
        
#         # bottom left corner
#         self.ctx.translate (0.0, 1.0)
#         self.ctx.move_to (0, 0)

#         self.normalize_scores()
#         frames = 100 - self.data["pointCount"]
#         curve_values = self.get_ease_out_curve(frames)
#         idx = 0
        
#         for c in curve_values:
#             for k, v in self.dataset.iteritems():
#                 # raw tuples (x, y)
#                 points = v["points"]
                
#                 # normalised values
#                 xpoints = v["xpoints"]
                
#                 x2 = xpoints[idx]
#                 if c > x2:
#                     idx += 1
#                     self.points[k] += v["points"][idx]
                
#                 p1, p2 = points[idx], points[idx+1]
#                 x1, x2 = xpoints[idx], xpoints[idx+1]

#                 # calculate draw coordinates for interpolated point
#                 x_value = maththings.normalise(t, x1, x2)
#                 x = maththings.to_value(x_value, p1[0], p[1])
#                 y = maththings.get_y(x, p1, p2)
                

    

#     def add_coordinate(self, team, team_data):
#         self.dataset[team]
        
                
                
            
    
#     def normalize_scores(self):
#         for k, v in self.dataset.iteritems():
#             self.points[k]["points"] = []
#             self.dataset[k]["xpoints"] = [maththings.normalize(p[0], self.data["xMin"], self.data["xMax"]) for p in v["points"]]

def create(data):
    graph = LineGraph(data)