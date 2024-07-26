import vec2 as v
import pygame

pygame.font.init()
text = pygame.font.SysFont("Verdana",40)

class slider:
    def __init__(self,name,start:v.vec,end:v.vec,range:tuple) -> None:
        self.start  = start
        self.end    = end
        self.range_start  = range[0]
        self.range_end    = range[1]

        self.pos = 0        # percentage of position between start and end
        self.name = name
        self.value = range[0]
        self.real_pos = 0   # real position of the dot

        # interaction

        self.hover = False
        self.hover_begin = None
        self.selected = False

        # visuals

        self.line_color =       (255,255,255)
        self.dot_color  =       (207, 204, 204)
        self.hover_color =      (150,150,150)
        self.selected_color =   (212, 161, 21)
        self.line_thickness =   4
        self.dot_radius  =      8

        self.alpha_surface =    pygame.surface.Surface([self.dot_radius*4]*2,pygame.SRCALPHA)
        self.alpha_surface.set_alpha(200)
        self.alpha_surface.convert_alpha()

    def update(self):
        """updates the slider (eg. calculates mouse interaction)"""
        connection = self.end.ret_sub(self.start)
        self.real_pos = self.start.ret_add(connection.ret_skalmul(self.pos))

        mouse = v.vec()
        mouse.from_list(pygame.mouse.get_pos())

        if mouse.distance(self.real_pos.pyg_center()) <= 14 or self.selected:
            if pygame.mouse.get_pressed()[0]:
                self.selected = True
            else:
                self.selected = False
                if not self.hover:
                    self.hover_begin = pygame.time.get_ticks()
                self.hover   = True
        else:
            self.selected   = False
            if self.hover:
                self.alpha_surface.fill((0,0,0,0))
            self.hover      = False

        if self.selected: # does the logic
            at = connection.skal(mouse.pyg_decenter().ret_sub(self.start))
            self.pos = at/connection.length()

            self.pos = 0 if self.pos < 0 else self.pos
            self.pos = 1 if self.pos > 1 else self.pos

            self.value = self.range_start+(self.range_end-self.range_start)*self.pos

    def render(self):
        converted_start = self.start.pyg_center()
        converted_end   = self.end.pyg_center()

        pygame.draw.line(pygame.display.get_surface(),(255,255,255),converted_start.to_list(),
                         converted_end.to_list(),self.line_thickness)
        
        def get_animation_value():
            time = pygame.time.get_ticks() - self.hover_begin
            animation_value = (time/100)**2
            return animation_value if animation_value <= 1 else 1

        if self.selected:

            dot_color = self.selected_color
            animation_value = get_animation_value()
        elif self.hover:

            dot_color = self.hover_color
            animation_value = get_animation_value()
        else:

            dot_color = self.dot_color

        dot_pos = self.real_pos.pyg_center()

        if self.selected or self.hover: # hovering circle with animaiton
            
            max_width = self.dot_radius*2
            pygame.draw.circle(self.alpha_surface,(60,60,60),v.vec(max_width,max_width).to_list(),max_width*animation_value)
            pygame.display.get_surface().blit(self.alpha_surface,dot_pos.ret_sub(v.vec(max_width,max_width)).to_list())

        pygame.draw.circle(pygame.display.get_surface(),dot_color,dot_pos.to_list(),self.dot_radius)
        
    def change_visuals(self,line_color=None,dot_color=None,hover_color=None,
                       selected_color=None,line_thickness:int=None,dot_radius:int=None):
        """change the values of the visual aspects of the sliders"""
        self.line_color =       line_color if line_color != None else self.line_color
        self.dot_color  =       dot_color if dot_color != None else self.dot_color
        self.hover_color =      hover_color if hover_color != None else self.hover_color
        self.selected_color =   selected_color if selected_color != None else self.selected_color
        self.line_thickness =   line_thickness if line_thickness != None else self.line_thickness
        self.dot_radius  =      dot_radius if dot_radius != None else self.dot_radius

    def get_name(self):
        """returns the name of the slider"""
        return self.name
    def get_value(self):
        return self.value
    def set_value(self,value):
        """set the value (and therefore the pos) of the slider (not tested yet)"""
        self.value  = value
        self.pos    = (value-self.range_start)/(-self.range_start+self.range_end)

class button:
    def __init__(self,name,pos:v.vec,width:float,text:str=None,call_function=None) -> None:
        """creates a simple button with animation. the visuals can be changed within the
        change_visuals mehtod. The button has the value True if clicked. Optional
        the button can call a function on clicking it. pos is the bootom right corner of the button"""

        self.pos        = pos
        self.text       = text if text != None else name
        self.name       = name
        self.width      = width             # for collision purposes
        self.height     = 50                # for collision static
        self.function   = call_function

        # interaction

        self.hover = False
        self.time_hover_begin = None
        self.pressed = False

        # visuals

        self.text_color             = (207, 204, 204)
        self.marker_hover_color     = (212, 161, 21)
        self.text_hover_color       = (150,150,150)

    def update(self):
        """updates the button (mouse input). has to be called each frame"""

        mouse = v.vec()
        mouse.from_list(pygame.mouse.get_pos())

        def check_collision():
            nonlocal mouse
            pos = self.pos.pyg_center()

            if mouse.x >= pos.x and mouse.x <= pos.x + self.width: #check x collision
                if mouse.y >= pos.y and mouse.y <= pos.y + self.height: # check y collision 
                    return True

            return False


        if check_collision():
            if pygame.mouse.get_pressed()[0]: # clicked
                self.pressed = True
            else:   # hover
                self.pressed = False
                if not self.hover:
                    self.time_hover_begin = pygame.time.get_ticks()
                self.hover   = True
        else: # not touched
            self.pressed   = False
            self.hover      = False
        
        # == does the logic == 
        if self.pressed: 
            if self.function != None:
                    self.function()
                    return

            self.value = True if self.pressed else False

    def render(self):
        global text
        pos = self.pos.pyg_center()
        
        if self.hover:
            time = pygame.time.get_ticks() - self.time_hover_begin
            animation_value = (time/100)**3
            if animation_value >= 1 : animation_value = 1

            pygame.draw.rect(pygame.display.get_surface(),self.marker_hover_color,(pos.x,pos.y+46-(40*animation_value),6,40*animation_value),0,4)
            pygame.display.get_surface().blit(text.render(self.text,True,self.text_hover_color),pos.ret_add(v.vec(10*animation_value,0)).to_list()) #,
        
        else:
            pygame.display.get_surface().blit(text.render(self.text,True,self.text_color),pos.ret_add(v.vec()).to_list())
            
    def change_visuals(self,text_color=None,marker_hover_color=None,text_hover_color=None):
        """change the values of the visual aspects of the sliders"""

        self.text_color             = text_color if text_color != None else self.text_color
        self.marker_hover_color     = marker_hover_color if marker_hover_color != None else self.marker_hover_color
        self.text_hover_color       = text_hover_color if text_hover_color != None else self.text_hover_color

    def get_name(self):
        """returns the name of the slider"""
        return self.name
    def get_value(self):
        return self.value
    def set_pos(self,pos):
        """pos has to be a value between 0 and 1"""
        self.pos = pos

class togglebutton:
    def __init__(self,name,pos:v.vec,width:float,text:str=None,call_function=None) -> None:
        """creates a 'toggle button' which bool value can be toggled by clicking"""

        self.pos        = pos
        self.text       = text if text != None else name
        self.name       = name
        self.width      = width             # for collision purposes
        self.height     = 50                # for collision static
        self.function   = call_function

        # interaction

        self.hover = False
        self.time_hover_begin = None
        self.pressed = False

        # visuals

        self.text_color             = (207, 204, 204)
        self.marker_hover_color     = (212, 161, 21)
        self.text_hover_color       = (150,150,150)

    def update(self):
        """updates the button (mouse input). has to be called each frame"""

        mouse = v.vec()
        mouse.from_list(pygame.mouse.get_pos())

        def check_collision():
            nonlocal mouse
            pos = self.pos.pyg_center()

            if mouse.x >= pos.x and mouse.x <= pos.x + self.width: #check x collision
                if mouse.y >= pos.y and mouse.y <= pos.y + self.height: # check y collision 
                    return True

            return False


        if check_collision():
            if pygame.mouse.get_pressed()[0]: # clicked
                self.pressed = True
            else:   # hover
                self.pressed = False
                if not self.hover:
                    self.time_hover_begin = pygame.time.get_ticks()
                self.hover   = True
        else: # not touched
            self.pressed   = False
            self.hover      = False
        
        # == does the logic == 
        if self.pressed: 
            if self.function != None:
                    self.function()
                    return

            self.value = True if self.pressed else False

    def render(self):
        global text
        pos = self.pos.pyg_center()
        
        if self.hover:
            time = pygame.time.get_ticks() - self.time_hover_begin
            animation_value = (time/100)**3
            if animation_value >= 1 : animation_value = 1

            pygame.draw.rect(pygame.display.get_surface(),self.marker_hover_color,(pos.x,pos.y+46-(40*animation_value),6,40*animation_value),0,4)
            pygame.display.get_surface().blit(text.render(self.text,True,self.text_hover_color),pos.ret_add(v.vec(10*animation_value,0)).to_list()) #,
        
        else:
            pygame.display.get_surface().blit(text.render(self.text,True,self.text_color),pos.ret_add(v.vec()).to_list())
            
    def change_visuals(self,text_color=None,marker_hover_color=None,text_hover_color=None):
        """change the values of the visual aspects of the sliders"""

        self.text_color             = text_color if text_color != None else self.text_color
        self.marker_hover_color     = marker_hover_color if marker_hover_color != None else self.marker_hover_color
        self.text_hover_color       = text_hover_color if text_hover_color != None else self.text_hover_color

    def get_name(self):
        """returns the name of the slider"""
        return self.name
    def get_value(self):
        return self.value
    def set_pos(self,pos):
        """pos has to be a value between 0 and 1"""
        self.pos = pos

class inputfield:
    pass

class loadingscreen:
    pass