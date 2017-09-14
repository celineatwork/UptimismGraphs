# import cairo, imageio, struct, maththings
import cairo, struct, maththings

class GraphObject(object):
    def __init__(self, data):
        self._data = data
        self._width = 1024
        self._height = 768
        self._surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, self._width, self._height)
        self._ctx = cairo.Context (self._surface)
        self._ims = None
        self.fnames = []
        self.fcount = 1

        # self.make_context()
    
    # def make_context(self):
        # makes the context
        # self._ctx.scale(self._width, self._height)
        # self._ctx.rectangle (0, 0, 1, 1)
        
        # bg = cairo.SolidPattern(1.0, 1.0, 1.0, 1.0)
        # self.ctx.set_source (bg)
        # self.ctx.fill ()

        # self.ctx.set_source_rgba (0, 0, 0, 0.5)
        # self.ctx.set_line_width (0.005)
        # self.ctx.translate (0.0, 1.0)
    
    def set_bg(self, url, gWidth, gHeight, offsetX, offsetY):
        self._surface = cairo.ImageSurface.create_from_png(url)
        self._ctx = cairo.Context(self._surface)
        self.ctx.set_source_surface(self._surface, 0.1, 0.1)

        gWidth, gHeight = float(gWidth), float(gHeight)
        sWidth, sHeight = float(self._surface.get_width()), float(self._surface.get_height())
        
        # set graph width and height
        self._ctx.scale(gWidth, gHeight)
        self._ctx.rectangle (1, 1, gWidth, gHeight)

        # put graph drawing field in allocated space
        self.ctx.translate (offsetX / gWidth, 1.0 + offsetY / gHeight)
        self._ctx.fill()

    def set_pen(self, line_width, hexstring, alpha=1.0):
        # self.set_color(hexstring, alpha)
        self.ctx.set_source_rgba (0, 0, 0, 1)
        self.ctx.set_line_width (line_width)

    def set_color(self, hexstring, alpha):
        # set pen color
        rgbstr = hexstring.replace("#", "")
        rgb = struct.unpack("BBB", rgbstr.decode('hex'))
        self._ctx.set_source_rgba(rgb[0], rgb[0], rgb[0], alpha)
    
    def draw_line(self, x, y):
        # draws a straight line and moves point to the end
        self._ctx.line_to(x, y)
        self._ctx.stroke_to_path()
        self._ctx.move_to(x, y)
        self._last_coord = Coordinate(x, y)
    
    def draw_curve(self, x, y):
        # draws a curved line and moves point to the end
        mX = ((self._last_coord.x + x)*1.01)/2.0
        mY = ((self._last_coord.y + y)*1.01)/2.0

        self._ctx.curve_to(self._last_coord.x, self._last_coord.y, mX, mY, x, y)
        self._ctx.stroke()
        self._ctx.move_to(x, y)
    
    def create_frame(self):
        fname = "pngs/img%s .png" % self.fcount
        self._surface.write_to_png(fname)
        self.fnames.append(fname)
        self.fcount += 1

    def create_gif(self, fps):
        images = [imageio.imread(f) for f in self.fnames]
        imageio.mimsave('graph.gif', images, fps=60)
    
    def get_ease_out_curve(self, frame_count):
        count, values, frame_count = 1.0, [0.0], float(frame_count)
        while count < frame_count:
            c = count / frame_count
            values.append( (2.0 * c) - (c ** 2.0) )
            count += 1.0
        values.append(1.0)
        return values
    
    @property
    def data(self):
        return self._data

    @property
    def dimensions(self):
        return (self._width, self._height)

    @property
    def surface(self):
        return self._surface
    
    @property
    def ctx(self):
        return self._ctx
    
    @property
    def last_coord(self):
        return self._last_coord

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
            # draw_points.append(Coordinate(p1.x, p1.y))
        return draw_points


    def print_coord(self):
        print [(d.x, d.y) for d in self.rawData]


        # y1, y2 = self.normalised[idx], self.normalised[idx+1]

        # interpY = maththings.normalize(t, y1, y2) 
        # cx = self.to_value(self.normalize(t, x1, x2), p1[0], p2[0])
        # cy = self.get_y(cx, p1, p2)

        # draw_points.append((cx, cy))
    
        # for p in draw_points:
        #     px = self.normalize(p[0], x_min, x_max) * 0.8
        #     py = self.normalize(p[1], y_min, y_max) * 0.8
        #     self.draw_line(px, -py)


class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cx = 0.0
        self.cy = 0.0
    
    def to_ratio(self, xMin, xMax, yMin, yMax, negX, negY):
        self.cx = normalise(self.x, xMin, xMax)
        self.cy = normalise(self.y, yMin, yMax)
        
        if negY:
            self.cy = self.cy * -1

        if negX:
            self.cx = self.cx * -1
        
        return Coordinate(self.cx, self.cy)
    
    @property
    def point(self):
        return (self.x, self.y)


# HELPER MATH FUNCTIONS
def normalise(c, cmin, cmax):
    c, cmin, cmax = float(c), float(cmin), float(cmax)
    return (c - cmin) / (cmax - cmin)

def to_value(t, n0, n1):
    return t * (n1 - n0) + n0

def get_y(x, p0, p1):
    return p0.y + (x - p0.x) * ( (p1.y - p0.y) / (p1.x - p0.x) )

def get_x(y, p0, p1):
    return ((p1.x - p0.x)/(p1.y - p0.y)) * (y - p0.y) + p0.x
    # return (x0 * y - x0 * y1 + x1 * y0) / (y0 - y1)