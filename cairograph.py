import cairo, imageio, struct, maththings

class GraphObject(object):
    def __init__(self, data):
        self._data = data
        self._width = 1024
        self._height = 768
        self._surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, self._width, self._height)
        self._ctx = cairo.Context (self._surface)
        self._last_coord = (0.0, 0.0)
        self.fnames = []
        self.fcount = 1

        self.make_context()
    
    def make_context(self):
        # makes the context
        self._ctx.scale(self._width, self._height)
        self._ctx.rectangle (0, 0, 1, 1)

        bg = cairo.SolidPattern(1.0, 1.0, 1.0, 1.0)
        self.ctx.set_source (bg)
        self.ctx.fill ()

        self.ctx.set_source_rgba (0, 0, 0, 0.5)
        self.ctx.set_line_width (0.005)
    
    def set_color(self, hexstring, alpha=1.0):
        # set pen color
        rgbstr = hexstring.replace("#", "")
        rgb = struct.unpack("BBB", rgbstr.decode('hex'))
        self._ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
    
    def draw_line(self, x, y):
        # draws a straight line and moves point to the end
        self._ctx.line_to(x, y)
        self._ctx.stroke()
        self._ctx.move_to(x, y)
        self._last_coord = (x, y)
    
    def create_frame(self):
        fname = "pngs/img%s .png" % self.fcount
        self._surface.write_to_png(fname)
        self.fnames.append(fname)
        self.fcount += 1

    def create_gif(self):
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
        self.rawData.append((x,y))

        if x < self.xMin or self.xMin is None:
            self.xMin = x
        if x > self.xMax or self.xMax is None:
            self.xMax = x 

        if y < self.yMin or self.yMin is None:
            self.yMin = y
        if y > self.yMax or self.yMax is None:
            self.yMax = y
    
    def normaliseY(self):
        self.normalised = map(lambda (x,y): maththings.normalize(y, self.yMin, self.yMax), self.rawData)
