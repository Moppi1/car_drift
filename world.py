# This function works like a camera. A given point (vec)
# gets transformed to the screen
import vec_2d as v


class world:
    def __init__(self) -> None:
        self.scale = 1
        self.pos  = v.vec()
    
    def set_zoom(self,value):
        self.scale = value
    def zoom(self,value):
        self.scale += value

    def set_pos(self,pos:v.vec):
        self.pos = pos
    def move(self,pos:v.vec):
        self.pos.add(pos)

    def transfrom(self, point):
        """transfroms all points (also lists) to the global space"""

        def to_c(p):
            return p.ret_sub(self.pos).ret_skalmul(self.scale)

        if type(point) == list:
            transformed_points = []
            for i in point:
                transformed_points.append(to_c(i))
            return transformed_points

        elif type(point) == v.vec:
            return to_c(point)
        
    def get_width(self,original): # get width of a line
        width = original*self.scale
        return width if width >= 1 else 1