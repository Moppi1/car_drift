import math
from pygame import display

#=== 2d vector class for the mathematical functions ===

class vec: 
    def __init__( self , x :float = 0 , y :float = 0):
        self.x = x
        self.y = y
    # leider etwas sehr "unordentlich" geworden
    def copy(self):
        return vec(self.x,self.y)
    def to_list(self):
        """converts vector x and y to list"""
        return (self.x,self.y)
    def from_list(self,tup):
        self.x = tup[0]
        self.y = tup[1]

    def length(self):
        """returns length of a vector (never 0 ?)"""
        #if self.x == 0 and self.y == 0 :
        #    #print("! Vector length is zero -> switching to close value !")
        #    new_x = 0.001 if self.x == 0 else self.x
        #    new_y = 0 if self.y == 0 else self.y
        #    return math.sqrt(new_x**2 + new_y**2)
        return math.sqrt(self.x**2 + self.y**2)

    def ret_add(self, pvec):
        """adds a second vec to this vec and returns"""

        return vec(self.x + pvec.x , self.y + pvec.y)
    def add(self, pvec):
        """adds a second vec to this vec"""

        self.x += pvec.x
        self.y += pvec.y

    def ret_sub(self,pvec):
        """subtracts a second vec from this vec and returns it"""
        return vec(self.x - pvec.x , self.y - pvec.y)
    def sub(self,pvec):
        """subtracts a second vec from this vec"""
        self.x -= pvec.x
        self.y -= pvec.y
    def distance(self,pvec):
        """returns the distance (float) between this vector and the other"""
        con = self.ret_sub(pvec)
        return con.length()

    def ret_rot(self,angle = 90):
        """returns this vec rotated by a given angle"""
        rot = math.radians(angle*-1)
        new_x = (math.cos(rot) * self.x - math.sin(rot) * self.y) 
        new_y = (math.sin(rot) * self.x + math.cos(rot) * self.y) 
        return vec(new_x , new_y)
    def rot(self,angle = 90):
        """sets this vec to 2D Axis rotation by a given angle"""
        rot = math.radians(angle*-1)
        new_x = (math.cos(rot) * self.x - math.sin(rot) * self.y) 
        new_y = (math.sin(rot) * self.x + math.cos(rot) * self.y) 
        self.x , self.y = new_x , new_y

    def mul(self,pvec):
        """muliplies the vector with an other vector"""

        self.x *= pvec.x
        self.y *= pvec.y
    def ret_skalmul(self,value):
        """muliplies the vector with a skal and returns"""
        return vec(self.x*value,self.y*value)
    def skalmul(self,value):
        """muliplies the vector with a skal and returns"""
        self.x *= value
        self.y *= value

    def ret_skaldiv(self,value):
        """muliplies the vector with a skal and returns"""
        return vec(self.x/value,self.y/value)
    def skaldiv(self,value):
        """divides the vector with a skalar and sets vec"""

        self.x /= value
        self.y /= value

    def skal(self,pvec,nor = True):
        """dot product (self vector gets normalized by default)"""
        if nor == True :
            nor = self.ret_nor()
            return nor.x * pvec.x + nor.y * pvec.y
        return self.x * pvec.x + self.y * pvec.y

    def cross(self,pvec):
        return self.x*pvec.y - pvec.x*self.y
    def ret_triple_cross(self,pvec):
        """Triple crossproduct"""
        z = self.x*pvec.y - pvec.x*self.y # z of first cross product
        x = self.y * z
        y = -z*self.x
        return vec(x,y)

    def ret_nor(self):
        """normalizes the vector (len=1) and return"""
        len = self.length()
        new_x = self.x / len
        new_y = self.y / len
        return vec(new_x,new_y)
    def nor(self):
        """normalizes the vector (len=1)"""
        len = self.length()
        self.x = self.x / len
        self.y = self.y / len

    def ret_nor_axis(self,axis:int):
        """normalizes the vector (x or y =1) along one axis and return"""
        len = self.x if axis == 1 else self.y
        new_x = self.x / len
        new_y = self.y / len
        return vec(new_x,new_y)
    def nor_axis(self,axis:int):
        """normalizes the vector (x or y =1) along one axis"""
        len = self.x if axis == 1 else self.y
        self.x /= len
        self.y /= len

    def ret_project(self,pvec):
        """projects vector 2 on vector 1"""
        return self.ret_nor().ret_skalmul(self.skal(pvec))
    def project(self,pvec):
        """projects vector 2 on vector 1"""
        self = self.ret_nor().mul(self.skal(pvec))

    def angle(self,pvec):
        """returns degree angle between 2 vectors"""
        angle = math.degrees(math.acos(self.skal(pvec,False)/(self.len() * pvec.len())))
        return angle

    def side(self,vec2):
        """get 1 / -1 if vec2 is right or left of main vec"""
        new_z = self.x * vec2.y + self.y * vec2.x
        return new_z / abs(new_z)

    def ret_mirror(self,center,axis):
        """not finished"""
        n = axis.ret_nor()
        con = self.ret_sub(center)
        mir = con.ret_skalmul(-1).ret_add(n.ret_skalmul(2*con.skal(axis,False)))
        # mirrored = -connectionvector + 2 * skalprod(n,con) * n

        return mir

    def pyg_center(self,):
        """translates the vector to the scuffed pygame coordinate system (from my to their coordiante system)"""
        return vec(self.x+(display.get_surface().get_width()//2),
                   -self.y+(display.get_surface().get_height()//2))
    def pyg_decenter(self,):
        """'de'centers the vector from the scuffed pygame coordinate system"""
        return vec(self.x-(display.get_surface().get_width()//2),
                   -self.y+(display.get_surface().get_height()//2))
    def __str__(self) -> str:
        return "x : "+ str(self.x) +" & y : "+ str(self.y)