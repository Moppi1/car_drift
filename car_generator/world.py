# This function works like a camera. A given point (vec)
# gets transformed to the screen
import vec2 as v


scale = 50
position = v.vec()

def set_zoom(value):
    global scale
    scale = value
def zoom(value):
    global scale
    scale += value
def set_pos(pos:v.vec):
    global position
    position = pos
def move(pos:v.vec):
    global position
    position.add(pos)
def transfrom(point):
    global position,scale
    """transfroms all points (also lists) to the global space"""
    def to_c(p):
        return p.ret_sub(position).ret_skalmul(scale)

    if type(point) == list or type(point) == tuple:
        transformed_points = []
        for i in point:
            transformed_points.append(to_c(i))
        return transformed_points
    elif type(point) == v.vec:
        return to_c(point)
    
def get_width(original): # get width of a line
    width = original*scale
    return width if width >= 1 else 1