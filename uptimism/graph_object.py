import cairo, struct, imageio
from uptimism.images import Images

class GraphObject(object):
    def __init__(self, data):
        self._data = data
        self._surface = None
        self._ctx = None
        self.fnames = []
        self.fcount = 1
    
    def set_surface_as_pattern(self, color, width, height):
        # makes a solid block color
        self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self._ctx = cairo.Context(self._surface)

        # color comes from colors.py 'Color' class
        self._ctx.set_source_rgb(color.r, color.g, color.b)
        self._ctx.paint()

        # scale and set draw point at bottom left
        self._ctx.scale(width, height)
        self._ctx.translate(0, 1)
    
    def set_surface_as_img(self, url):
        self._surface = self.load_png(url)
        self._ctx = cairo.Context(self._surface)
        self._ctx.set_source_surface(self._surface)
        self._ctx.paint()

        self._ctx.scale(self._surface.get_width(), self._surface.get_height())
        self._ctx.translate(0, 1)
    
    def reset_bg(self, url):
        ctx = cairo.Context(self._surface)
        ctx.set_source_surface(self.load_png(url))
        ctx.paint()

    def set_pen(self, line_width, color, alpha=1.0):
        # color comes from colors.py 'Color' class
        self._ctx.set_source_rgba(color.r, color.g, color.b, alpha)
        self._ctx.set_line_width (line_width)
    
    def draw_line(self, x, y):
        # draws a straight line and moves pen to the end
        self._ctx.line_to(x, y)
        self._ctx.stroke()
        self._ctx.move_to(x, y)
    
    def write_text(self, text_list):
        font_size = 100
        padding = 50
        line_height = 1.2

        ctx = cairo.Context(self._surface)
        ctx.select_font_face ("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(font_size)
        ctx.set_source_rgb (1, 1, 1)

        x, y = padding, (padding + font_size)

        for line in text_list:
            ctx.move_to (x, y)
            ctx.show_text (line)
            y += font_size * line_height
    
    # def write_line(self, line):
    #     font_size = 100
    #     padding = 50
    #     line_height = 1.2

    #     ctx = cairo.Context(self._surface)
    #     ctx.select_font_face ("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    #     ctx.set_font_size(font_size)
    #     ctx.set_source_rgb (1, 1, 1)

    #     x, y = padding, (padding + font_size)
    #     ctx.move_to (x, y)
    #     ctx.show_text (line)
    #     y += font_size * line_height

    
    def draw_img(self, img, x, y):
        ctx = cairo.Context(self._surface)
        ctx.translate(x, y)
        ctx.set_source_surface(img)
        ctx.paint()
    
    def create_frame(self):
        fname = "pngs/img%s .png" % self.fcount
        self._surface.write_to_png(fname)
        self.fnames.append(fname)
        self.fcount += 1

    def create_gif(self, fps):
        images = [imageio.imread(f) for f in self.fnames]
        imageio.mimsave('graph.gif', images, fps=fps)
    
    def get_ease_out_curve(self, frame_count):
        count, values, frame_count = 1.0, [0.0], float(frame_count)
        while count < frame_count:
            c = count / frame_count
            values.append( (2.0 * c) - (c ** 2.0) )
            count += 1.0
        values.append(1.0)
        return values
    
    def load_png(self, fname):
        return cairo.ImageSurface.create_from_png(open(fname, 'rb'))
    
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

    @property
    def dimensions(self):
        return self._surface.get_width(), self._surface.get_height()

    # def set_surface_as_img(self, bgImg, headerImg, plotImg):
    #     # set background
    #     self._surface = self.load_png(bgImg)
    #     self._ctx = cairo.Context(self._surface)

    #     # add header with team names
    #     self._ctx.set_source_surface(self.load_png(headerImg))
    #     self._ctx.paint()

    #     # add graph plot
    #     plot = self.load_png(plotImg)
    #     sW, sH = float(self._surface.get_width()), float(self._surface.get_height())
    #     pW, pH = float(plot.get_width()), float(plot.get_height())
    #     xOffset = (sW - pW)/2
    #     yOffset = (sH - pH)/2 + 100

    #     self._ctx.translate(xOffset, yOffset)
    #     self._ctx.set_source_surface(plot)
    #     self._ctx.paint()

    #     self._ctx.scale(pW, pH)
    #     # set starting position at bottom left
    #     # self._ctx.translate(0.0, 1.0)