def normalize(c, cmin, cmax):
    c, cmin, cmax = float(c), float(cmin), float(cmax)
    return (c - cmin) / (cmax - cmin)

def to_value(p, v1, v2):
    return p * (v2 - v1) + v1

def get_y(x, p1, p2):
    x0, y0, x1, y1 = p1[0], p1[1], p2[0], p2[1]
    return y0 + (x - x0) * ( (y1 - y0) / (x1 - x0) )

def get_x(y, p1, p2):
    x0, y0, x1, y1 = p1[0], p1[1], p2[0], p2[1]
    # print y0, y, y1
    return x0 + (y - y0) * ( (x1 - x0) / (y1 - y0) )
    # return (x0 * y - x0 * y1 + x1 * y0) / (y0 - y1)