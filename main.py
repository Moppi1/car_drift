import draw as d 
import vec_2d as v
import car as c
import world as w





def main():
    d.window((2560,720*1.5),"")
    sportcar = c.car(6)
    sportcar.create_geometry()
    space = w.world()
    space.set_zoom(50)
    
    if not d.controller_init(): raise("Kein Controller verbunden : - (")

    dt = 0.01

    while True:
        d.clear((50, 64, 37))
        if d.key("q"):
            space.zoom(10*dt)
        if d.key("e"):
            space.zoom(-10*dt)
        if d.key("w"):
            space.move(v.vec(0,10*dt))
        if d.key("s"):
            space.move(v.vec(0,-10*dt))
        
        sportcar.steering = d.controller_axis(2)*45

        sportcar.render(space)
        sportcar.render_debug(space)

        

        dt = d.delta_time()/1000
        print(1000/(dt*1000)) #fps
        
        d.update()

if __name__ == "__main__":
    main()
