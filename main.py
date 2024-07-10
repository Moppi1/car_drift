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
    
    test = d.load_image("Blender/transparency_test.png")
    d.image_transform(test)

    dt = 0.01

    while True:
        d.clear((50, 64, 37))
        d.render_image(test,v.vec())
        if d.key("q"):
            space.zoom(10*dt)
        if d.key("e"):
            space.zoom(-10*dt)
        if d.key("w"):
            space.move(v.vec(0,10*dt))
        if d.key("s"):
            space.move(v.vec(0,-10*dt))
        

        sportcar.render(space)

        

        dt = d.delta_time()/1000
        print(1000/(dt*1000))
        
        d.update()

if __name__ == "__main__":
    main()
