import pygame
import pygame.gfxdraw
import vec2 as v
import gui.element as e
import gui.gui_handler as g
import car_generator.car as c
import car_generator.checkerboard as b
#pygame.font.init()


pygame.init()

clock = pygame.time.Clock()

def main():
    
    width = 2560
    height = 1080
    window = pygame.display.set_mode((width,height))

    def ui_cycle():
        nonlocal ux , board
        board.render(40,v.vec(0,ux.get_element_value("test1")))
        ux.update()
        pygame.draw.circle(pygame.display.get_surface(),(230,230,89,),[1280,540],10)
        
        sportcar.steer(ux.get_element_value("test2"))
        sportcar.render()
        sportcar.render_debug(show_steering=True)

    ux = g.gui("main")
    ux.element_append(e.slider("test1",v.vec(400,400),v.vec(400,-400),[200,-100]))
    ux.element_append(e.slider("test2",v.vec(-200,-400),v.vec(200,-400),[45,-45]))
    ux.get_element("test1").set_value(0)
    ux.get_element("test2").set_value(0)
    ux.element_append(e.button("test_b1",v.vec(-1000,100),400,"ok mal was anderes"))
    ux.element_append(e.button("test_b2",v.vec(-1000,150),400))
    ux.element_append(e.button("test_b3",v.vec(-1000,200),400,"bitte lass es funktionieren"))
    ux.element_append(e.button("test_b4",v.vec(-1000,250),400,"performance"))
    ux.element_append(e.button("test_b5",v.vec(-1000,300),400,"power"))
    ux.element_append(e.button("test_b6",v.vec(-1000,350),400,"energy"))

    board = b.checkerboard([10,30],(160,160,160))
    sportcar = c.car(6)
    sportcar.create_geometry()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        window.fill((38,50,56))

        #image = pygame.image.load("gui/default_full_screen.png").convert()
        #window.blit(image,v.vec().to_list())
        
        ui_cycle()
        pygame.display.set_caption(str(round(1000/clock.tick())))

        
        pos = v.vec().pyg_center()
        pygame.display.flip()




if __name__ == "__main__":
    
    main()