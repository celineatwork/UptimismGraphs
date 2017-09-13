#!/usr/bin/env python

import math
import imageio
import cairo
import time

class GraphType():
    LINEGRAPH = u"lineGraph"
    BARGRAPH = u"barGraph"
    GAUGEGRAPH = u"gaugeGraph"

class LineGraph():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, self.width, self.height)
        self.ctx = cairo.Context (self.surface)
        self.current = (0, 0)
        self.fnames = []
        self.count = 1
        self.make_context()

    def make_context(self):
        bg = cairo.SolidPattern(1.0, 1.0, 1.0, 1.0)
        self.ctx.scale(self.width, self.height)
        self.ctx.rectangle (0, 0, 1, 1)
        self.ctx.set_source (bg)
        self.ctx.fill ()
        self.draw_axis()
    
    def draw_axis(self):
        self.ctx.set_source_rgba (0, 0, 0, 0.5)
        self.ctx.set_line_width (0.005)

        # draw x axis
        self.ctx.translate (0.1, 0.9)
        self.ctx.move_to (0, 0)
        self.ctx.line_to (0.8, 0)
        self.ctx.stroke()

        # draw y axis
        self.ctx.move_to (0, 0)
        self.ctx.line_to (0, -0.8)
        self.ctx.stroke()

        # make image
        self.create_image()
        self.count += 1
    
    def draw_graph(self, data):
        self.ctx.move_to (0, 0)
        points = data["dataPoints"]

        x_min = float(data["x_min"])
        x_max = float(data["x_max"])
        
        y_min = float(data["y_min"])
        y_max = float(data["y_max"])

        idx = 0
        frame_count = 101 - len(points)
        
        normalized_x_points = []
        normalized_y_points = []
        draw_points = []

        for p in points:
            normalized_x_points.append(self.normalize(p[0], x_min, x_max))
        
        time_points = get_interpolation(frame_count)
        
         # draw to points[0]

        for t in time_points:
            x2 = normalized_x_points[idx+1]
            
            if t > x2:
                idx += 1
                draw_points.append(points[idx])
            
            p1, p2 = points[idx], points[idx+1]
            x1, x2 = normalized_x_points[idx], normalized_x_points[idx+1]
            cx = self.to_value(self.normalize(t, x1, x2), p1[0], p2[0])
            cy = self.get_y(cx, p1, p2)

            draw_points.append((cx, cy))
        
        for p in draw_points:
            px = self.normalize(p[0], x_min, x_max) * 0.8
            py = self.normalize(p[1], y_min, y_max) * 0.8
            self.draw_line(px, -py)
        
        self.create_gif()

    def normalize(self, c, cmin, cmax):
        return (c - cmin) / (cmax - cmin)

    def to_value(self, p, v1, v2):
        return p * (v2 - v1) + v1

    def get_y(self, x, c1, c2):
        x0, y0, x1, y1 = c1[0], c1[1], c2[0], c2[1]
        return y0 + (x - x0) * ( (y1 - y0) / (x1 - x0) )
    
    def draw_line(self, x, y):
        print (x, y)
        self.ctx.line_to(x, y)
        self.ctx.stroke()

        self.ctx.move_to(x, y)
        self.create_image()

        # print(self.count, round(x, 4), round(y, 4))
        self.current = (x, y)
        self.count += 1
        
    def create_image(self):
        fname = "pngs/img%s .png" % self.count
        self.surface.write_to_png(fname)
        self.fnames.append(fname)
    
    def create_gif(self):
        print "Making gif"
        images = []
        for filename in self.fnames:
            images.append(imageio.imread(filename))
        imageio.mimsave('graph.gif', images, fps=60)




def get_interpolation(duration):
    count = 1.0
    values = [0]

    while count < duration:
        c = count / duration
        # shift = (3.0 * c ** 2.0) - (2.0 * c ** 3.0)
        shift = (2.0 * c) - (c ** 2.0)
        values.append(shift)
        count += 1.0
    return values

def get_idx(v, vlist):
    for i in range(len(vlist)):
        if v <= vlist[i]:
            return i


def make_image():
    data = {
    "type": "lineGraph",
    "width": 1024,
    "height": 768,
    "y_min": 100,
    "x_min": 2001,
    "y_max": 30000,
    "x_max" : 2007,
    "dataPoints": [(2001, 100), (2002, 30000), (2003, 19700), (2004, 17500), (2005, 14500), (2006, 10000), (2007, 5800)]
    }

    if data["type"] == GraphType.LINEGRAPH:
        graph = LineGraph(data["width"], data["height"])
        graph.draw_graph(data)

make_image()