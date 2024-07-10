import pygame
import pygame.gfxdraw
import vec_2d

pygame.init()
pygame.font.init()
pygame.display.init()
pygame.mixer.init()

#important setting variabels (default)
screen = height = width  = clock = 0
change_width = change_height = 0


#This code is used to recreate the simpel funtions of the GTR and to avoid pygames strange coordinate system

# ====== essential ======

def window(res:tuple,name="tengine",path:str=None):
    """creates the window for pygame"""
    
    global screen, height, width , clock
    global change_height , change_width
    width = res[0]
    height= res[1]

    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((res[0],res[1]))
    if path != None :
        Icon = pygame.image.load(path)
        pygame.display.set_icon(Icon)
    screen.fill((241, 252, 255))

    pygame.display.set_caption(name)

    change_width = width // 2 #constant for transforming width
    change_height = height // 2 #constant for transforming height
def get_window_dimensions():
    """returns height and width as tuple"""
    return (height,width)
def window_setname(name=""):
    """sets name of the current window"""
    pygame.display.set_caption(name)
def window_seticon(path : str):
    """loads window icon from path"""
    Icon = pygame.image.load(path)
    pygame.display.set_icon(Icon)

def update():
    """flips the screen (updates whole screen)
    and tests if window gets closed"""
    pygame.display.flip()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()

def delta_time(framerate=0):
    return clock.tick(framerate)

# ========== input ==========

def key(k):
    """test if key (k) is pressed"""
    key = pygame.key.get_pressed()
    if key[pygame.key.key_code(k)] == True:
        return True
    else: return False

def mouse(corrected : bool = True ):
    """returns x and y of mouse pos"""
    x , y = pygame.mouse.get_pos()
    if corrected: 
        return (x - width // 2,(y - height // 2)*-1)
    return (x,y)
def mouse_clicked(k = 0):
    return pygame.mouse.get_pressed()[k]

# controler input

def controller_init():
    pygame.joystick.init()
    try:
        global joysticks
        joysticks = pygame.joystick.Joystick(0)
        return True
    except:
        return False

def controller_name():
    """get the name of the current controller device"""
    joysticks.get_name()

def controller_axis(axis=0):
    "get the deflection of the joysticks and the trigger"
    return joysticks.get_axis(axis)

def controller_button(n = 0):
    """n controls the detected button : a,b,x,y,lo,ro, view , menu , stickl ,stickr"""
    return joysticks.get_button(n)

def controller_arrow(n = 0):
    """get the input of the directional pad"""
    return joysticks.get_hat(n)

def controller_vibrate(strength,duration:int):
    """vibrate the controller for a specific time (in ms)"""
    joysticks.rumble(strength,strength,duration)

# ====== draw functions ======

def clear(color=((255,255,255))):
    screen.fill(color)

def rectangle(pos : vec_2d.vec = vec_2d.vec(0,0) ,wid=50,hei=10,w=0,color=(0,0,0),round=0):
    """draws an rectangle at give pos if w = 0 the rec will be filled and \n
    if round = 1 corners get rounded"""
    round = int(round)
    p_x = int(pos.x + width // 2)
    p_y = int((pos.y - height // 2)*-1)
    pygame.draw.rect(screen , color , (p_x,p_y,wid,hei) , int(w) , int(round),-1,-1,-1,-1)

def circle(pos : vec_2d.vec,rad=100,color=(0,0,0),w=1,anti=False):
    """draws an outline of a circle at pos (vec2_d) with the radius and a color(default : black)
    and a specified width
    ----
    the circle can also be antialised if anti = True
    """
    pos = (int(pos.x + width // 2) , int((pos.y - height // 2)*-1)) #FCK PYG

    if anti:
        pygame.gfxdraw.aacircle(screen,pos[0],pos[1],rad,color)
    else:
        pygame.draw.circle(screen,color,pos,rad,int(w))
def fill_circle(pos : vec_2d.vec,rad=10,color=(0,0,0),anti=False):
    """draws a filled circle at x , y with the radius and a color(default : black)

    ----
    the circle can also be antialised if anti = True
    """
    pos = (int(pos.x + width // 2) , int((pos.y - height // 2)*-1)) #FCK PYG

    if anti:
        pygame.gfxdraw.filled_circle(screen,pos[0],pos[1],int(rad),color)
        pygame.gfxdraw.aacircle(screen,pos[0],pos[1],int(rad),color)
    else:
        pygame.draw.circle(screen,color,pos,rad)

def polygon(vl,color=(0,0,0),w=1,anti=False):
    """draws an unfilled polygon from given coords e.g. [ vec1, vec2 , ...]"""
    clr = [] # list of x - y coords
    for i in vl:
        x = int(i.x + width // 2)
        y = int((i.y - height // 2)*-1)
        clr.append((x,y))
    if anti:
        pygame.gfxdraw.aapolygon(screen,clr,color)
    else:
        pygame.draw.polygon(screen,color,clr,int(w))
def fill_polygon(vl,color=(0,0,0),w=0,anti=False):
    """draws an filled polygon from given coords e.g. [ vec1, vec2 , ...]"""
    clr = []
    for i in vl:
        x = int(i.x + change_width)
        y = int((i.y - change_height)*-1)
        clr.append((x,y))
    if anti:
        pygame.gfxdraw.filled_polygon(screen,clr,color)
        pygame.gfxdraw.aapolygon(screen,clr,color)
    else:
        pygame.draw.polygon(screen,color,clr,int(w))

def line(p1 : vec_2d.vec ,p2 : vec_2d.vec,w=3,color=(0,0,0),anti=False):
    """draws a line between p1 , p2   e.g. vec1 , vec2 """
    p1 = (int(p1.x + width // 2) , int((p1.y - height // 2)*-1))
    p2 = (int(p2.x + width // 2) , int((p2.y - height // 2)*-1))

    if anti:
        pygame.draw.aaline(screen,color,p1,p2)
    pygame.draw.line(screen,color,p1,p2,int(w))

def text(pos : vec_2d.vec,text,size=30,anti=True,ptype="Ariel",colorf=(0, 0, 0),colorb=None):
    """prints text at x,y (font could be changed)"""
    font   = pygame.font.SysFont(ptype, 30)
    text = font.render(text,anti,colorf,colorb)
    screen.blit(text,(pos.x + width // 2,(pos.y - height // 2)*-1))

# image

def load_image(path:str):
    """get an 'image' object which can be blit to screen with image()"""
    return pygame.image.load(r""+path)

def image_transform(image ,s=1 , r=0):
    image = pygame.transform.rotozoom(image.convert_alpha(),r,s) # zooming

def render_image(image,pos : vec_2d.vec):
    """prints an image at a vec pos"""
    h = image.get_height()/2  #for centering
    w = image.get_width()/2   # "
    screen.blit(image.convert_alpha(),((pos.x + width // 2)-w,((pos.y - height // 2)*-1)-h))

def pixel_image(path:str,pos : vec_2d.vec,s=1):
    """draws an pixellated (non blended ) image """

    im = pygame.image.load(r""+path)
    h = s / 2  #for centering
    w = s / 2   # "
    im = pygame.transform.scale(im.convert(),(s,s))
    screen.blit(im,((pos.x + w + width // 2)  , ((pos.y + h - height // 2)*-1)) )

# ====== sound (wip) ======

def sound(path,volume=1,loop=0):
    """plays a sound from a given path and by a given volume
    ---- (volume = 1 means default value , loop = -1 means infinite looping)
    """
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)   #sets volume of sound
    sound.play(loop) # sound gets looped if loop = -1