import cairo, struct, imageio

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from uptimism.images import Images
from uptimism.colors import Colors
import uptimism.text_writer as Writer

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
    
    def write_text(self, text_list, bg=None, font_size=100, padding=50, line_height=1.2):
        if bg is None:
            bg = self._surface

        x, y = 0, 0
        images = Writer.get_text_images(text_list, font_size, padding, line_height)

        for i in range(len(images)):
            img = images[i]
            self.draw_img(x, y, img, bg)
            y += font_size * line_height

            # if i == 1:
            #     y += padding
                
    
    def draw_img(self, x, y, fg, bg=None):
        if bg is None:
            bg = self._surface

        ctx = cairo.Context(bg)
        ctx.translate(x, y)
        ctx.set_source_surface(fg)
        ctx.paint()
    
    def load_bar_img(self, url, text):
        surface = self.load_png(url)
        
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