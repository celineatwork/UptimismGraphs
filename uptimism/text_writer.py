from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cairo

def create_text_img(line, font_face, img_size, xOffset, yOffset):
    CLEAR_WHITE = (255,255,255,0)
    SOLID_WHITE = (255,255,255,255)
    SOLID_RED = (255, 0, 0, 255)

    img = Image.new("RGBA", img_size, SOLID_RED)
    d = ImageDraw.Draw(img)
    # d.text((0, 0), line, font=font_face, fill=SOLID_WHITE)
    print line

    d.text((xOffset, yOffset), line, font=font_face, fill=SOLID_WHITE)

    # save png into mem buffer
    f = BytesIO()
    img.save(f, "png")
    f.seek(0)

    # clean up some memory eagerly
    del img
    del d

    return f

def get_text_images(text_list, font_size, padding, line_height):
    font_face = ImageFont.truetype("assets/Gotham-Narrow-Book.ttf", font_size)
    xOffset, yOffset = padding, 0.0
    images = []
    
    # add padding on top if i = 0

    for i in range(len(text_list)):
        line = text_list[i]
        width = int(font_size*0.62) * len(line) + padding
        height = int(font_size * line_height)

        # if i == 0:
        #     height += padding
        #     yOffset = padding

        img_size = (width, height)

        f = create_text_img(line, font_face, img_size, xOffset, yOffset)
        images.append(cairo.ImageSurface.create_from_png(f))
        del f

    return images

# def write_text(self, text_list):
#     # font_size = 100
#     # padding = 50
#     # line_height = 1.2

#     # ctx = cairo.Context(self._surface)
#     # ctx.select_font_face ("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
#     # ctx.set_font_size(font_size)
#     # ctx.set_source_rgb (1, 1, 1)

#     # x, y = padding, (padding + font_size)

#     # for line in text_list:
#     #     ctx.move_to (x, y)
#     #     ctx.show_text (line)
#     #     y += font_size * line_height

#     font_size = 100
#     padding = 50
#     line_height = 1.2

#     font_face = ImageFont.truetype("assets/Gotham-Narrow-Book.ttf", font_size)
#     img_size = (self._surface.get_width(), font_size)

#     x, y = padding, padding
    
#     for line in text_list:
#         f = create_text_img(line, font_face, img_size)
#         surface = cairo.ImageSurface.create_from_png(f)
#         del f

#         self.draw_img(surface, x, y)
#         y += font_size * line_height

# def create_text_img(line, font_face, img_size):
#     CLEAR_WHITE = (255,255,255,0)
#     SOLID_WHITE = (255,255,255,255)

#     img = Image.new("RGBA", img_size, CLEAR_WHITE)
#     d = ImageDraw.Draw(img)
#     d.text((0, 0), line, font=font_face, fill=SOLID_WHITE)

#     # save png into mem buffer
#     f = BytesIO()
#     img.save(f, "png")
#     f.seek(0)

#     # clean up some memory eagerly
#     del img
#     del d

#     return f

# def load_bar_img(url, text):
    


