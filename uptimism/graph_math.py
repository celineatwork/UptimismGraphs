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