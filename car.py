import vec_2d as v
import draw as d
import world as w
from math import atan , tan , degrees , radians

class car:
    def __init__(self,length=1) -> None:
        self.length = length
        self.pos = v.vec()
        self.cog = v.vec()  #center of gravity
        self.rot = 0
        self.steering = 0


    def create_geometry(self): #generates the geometry of the car

        length      = self.length

        # ==== BODY ====

        front_width_b = 0.64
        rear_width  = 1.2
        mid_width   = 2
        ratio       = 0.4     # length of stern %
        steep       = 0.01
        

        def get_width_at(y_p:float): # get with of baseshape at percentage (1 = front)
            start   = v.vec(front_width_b/2,length)
            end     = v.vec(rear_width/2,0)

            con     = end.ret_sub(start)
            con.skaldiv(con.y)
            
            return end.ret_add(con.ret_skalmul(self.length*y_p)).x

        body_p =    [v.vec(-front_width_b/2,length/2),                      # front left
                     v.vec(front_width_b/2,length/2),                       # front right
                     v.vec(get_width_at(0.3),length*(-0.5+ratio+steep)),    # mid small right
                     v.vec(mid_width/2,length*(-0.5+ratio)),                # mid right 
                     v.vec(rear_width/2,-length/2),                         # back right
                     v.vec(-rear_width/2,-length/2),                        # back left
                     v.vec(-mid_width/2,length*(-0.5+ratio)),               # mid left
                     v.vec(-get_width_at(0.3),length*(-0.5+ratio+steep))]   # mid small left

        def total_width_at(y_p:float): # get with of baseshape at percentage (1 = front)
            #searches for segment from front to rear

            y = length*(-0.5+y_p) # y coord

            start = v.vec(rear_width/2,-length/2) # first y coord of front

            for i in range(1,5):
                if  y <= start.y and y >= body_p[i].y:
                    end = body_p[i]
                else:
                    start = body_p[i]
            
            con     = end.ret_sub(start)
            con.skaldiv(con.y)

            return end.ret_add(con.ret_skalmul(self.length*y_p)).x

        # ==== SUSPENSION ====

        front_pos = 0.92 #percentage distance from rear to front edge
        rear_pos =  0.11 # percentage distance from rear to rear edge
        length_rs = 0.56 # length (y) of rear suspension
        length_fs = 0.42
        tip = 0.76 # scaling factor of the tip of suspension
        width_s = 1.54 # total width of suspension on x

        suspension_rear_pr =     [v.vec(total_width_at(rear_pos),length*(-0.5+rear_pos)),        # lower bodypoint
                                 v.vec(total_width_at(rear_pos+(length_rs/length)),length*(-0.5+rear_pos)+length_rs),       # upper bodypoint
                                 v.vec(width_s,length*(-0.5+rear_pos)+length_rs),               # upper point
                                 v.vec(width_s,length*(-0.5+rear_pos)+length_rs*(1-tip))]       # lower point

        suspension_front_pr =     [v.vec(total_width_at(front_pos),length*(-0.5+front_pos)),     # upper bodypoint
                                  v.vec(total_width_at(front_pos-(length_fs/length)),length*(-0.5+front_pos)-length_fs),    # lower bodypoint
                                  v.vec(width_s,length*(-0.5+front_pos)-length_fs*(tip)),       #lower point        
                                  v.vec(width_s,length*(-0.5+front_pos))]                       # upper point


        # ==== WHEEL ====

        wheel_width  = 0.57
        wheel_radius = 1.17/2
        corner       = 0.1
        r = v.vec(-corner,0)

        tire  = []
        
        #generate one wheel
        for i in range(4):
            if i == 0: p = v.vec((-wheel_width/2)+corner,wheel_radius-corner)
            if i == 1: p = v.vec((wheel_width/2)-corner,wheel_radius-corner)  
            if i == 2: p = v.vec((wheel_width/2)-corner,-wheel_radius+corner)
            if i == 3: p = v.vec((-wheel_width/2)+corner,-wheel_radius+corner)
            c = p.ret_add(r)
            tire.append(c)
            for j in range(2):
                r.rot(45)
                c = p.ret_add(r)
                tire.append(c)

        # other wheels
        distance = 0.9 # moving wheels in by percentage 
        tire_pos = [v.vec(width_s*distance+wheel_width/2,length*(-0.5+front_pos)-(length_fs*tip/2)),
                    v.vec(-width_s*distance-wheel_width/2,length*(-0.5+front_pos)-(length_fs*tip/2)),
                    v.vec(width_s*distance+wheel_width/2,length*(-0.5+rear_pos)+(length_rs*(1-tip/2))),
                    v.vec(-width_s*distance-wheel_width/2,length*(-0.5+rear_pos)+(length_rs*(1-tip/2)))]


        self.body = body_p
        self.suspension_f = suspension_front_pr
        self.suspension_r = suspension_rear_pr
        self.tire   = tire
        self.tire_pos = tire_pos
        self.wheelbase = length*(front_pos-rear_pos) -(length_fs*tip/2)-(length_rs*(1-tip/2))
        self.width = width_s*distance+wheel_width/2

    # math and physics

    def _steering_wheels(self):
        """returns the individual steering angles of the wheels (left and right)"""
        if self.steering == 0:
            return 0,0

        radius = self.wheelbase/tan(radians(self.steering))

        al = degrees(atan(self.wheelbase/(radius+self.width)))
        ar = degrees(atan(self.wheelbase/(radius-self.width)))

        return al , ar



    # rendering

    def render(self,world:w.world):

        self.facing = v.vec(0,1).ret_rot(self.rot) # can very likely be removed later
        wl = world.get_width(0.04)  # line thickness

        #suspension
        for i in range(len(self.suspension_r)):
            for j in range(i+1,len(self.suspension_r)):
                #Rear supspension
                d.line(world.transfrom(self.suspension_r[i]),world.transfrom(self.suspension_r[j]),wl,(32, 32, 32))
                d.line(world.transfrom(self.suspension_r[i].ret_mirror(v.vec(),self.facing)),
                       world.transfrom(self.suspension_r[j].ret_mirror(v.vec(),self.facing)),wl,(32, 32, 32))
                #front suspension
                d.line(world.transfrom(self.suspension_f[i]),world.transfrom(self.suspension_f[j]),wl,(32, 32, 32))
                d.line(world.transfrom(self.suspension_f[i].ret_mirror(v.vec(),self.facing)),
                       world.transfrom(self.suspension_f[j].ret_mirror(v.vec(),self.facing)),wl,(32, 32, 32))
                
        #body
        d.fill_polygon(world.transfrom(self.body),(255, 255, 255),anti=True)

        #wheels
        steering_l , steering_r = self._steering_wheels()

        for i in self.tire_pos:
            points  = []
            for j in self.tire:
                if   i.y > 0 and i.x <= 0:      # front_left
                    points.append(world.transfrom(j.ret_rot(steering_l).ret_add(i)))
                elif i.y > 0 and i.x >= 0:      # front_right
                    points.append(world.transfrom(j.ret_rot(steering_r).ret_add(i)))
                else:                           # rear wheels
                    points.append(world.transfrom(j.ret_add(i)))
            d.fill_polygon(points,(25,25,25),anti=True)


    
    def render_debug(self,world):
        #center of gravity
        #d.fill_circle(self.cog)

        #steering
        sl , sr = self._steering_wheels()
        r =  world.transfrom(self.tire_pos[0].ret_add(v.vec(1,0).ret_rot(sr).ret_skalmul(1000)))
        d.line(world.transfrom(self.tire_pos[0]),r,2,(200,200,200))

        l =  world.transfrom(self.tire_pos[1].ret_add(v.vec(1,0).ret_rot(sl).ret_skalmul(1000)))
        d.line(world.transfrom(self.tire_pos[1]),l,2,(200,200,200))

        d.line(world.transfrom(self.tire_pos[3]),world.transfrom(v.vec(1000,self.tire_pos[3].y)),2,(180,180,180))


    def move(self,dist):
        self.pos.add(dist)
