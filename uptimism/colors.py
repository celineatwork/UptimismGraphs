class Color():
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class Colors():
    # maybe good to put team colors here?
    WHITE = Color(1.0, 1.0, 1.0, 1.0)
    BLACK = Color(0.0, 0.0, 0.0, 1.0)
    GRAY = Color(0.6, 0.6, 0.6, 1.0)
    TRANSPARENT = Color(0.0, 0.0, 0.0, 0.0)