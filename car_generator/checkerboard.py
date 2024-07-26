import pygame
import vec2 as v

class checkerboard:
    def __init__(self,dimensions:list,color=(255,255,255)) -> None:
        """generate 'blueprint' checkerboard with a variable int x and y size
        (needs a performance overhaul)"""
        self.dimensions = dimensions
        self.checkerboard = []
        self.color      = color

        self._generate_pattern()

    def _generate_pattern(self):
        started = 0
        last = 0
        width = self.dimensions[0]
        height = self.dimensions[1]

        row = []
        for x in range(width):
            for y in range(height):

                if last == 0:   last = 1
                else :          last = 0
                row.append(False) if last == 0 else row.append(v.vec( x-(width//2),y-(height//2)+1 ))
            
            if started == 0:    last = started = 1
            else:               last = started = 0

            self.checkerboard.append(row)
            row = []

    def render(self,size,shift):
        x = shift.x % size*2
        y = shift.y % size*2

        for row in self.checkerboard:
            for tile in row:
                if tile != False:
                    real_pos = v.vec(x+(tile.x*size),y+(tile.y*size)).pyg_center()
                    pygame.draw.rect(pygame.display.get_surface(),self.color,(real_pos.x,real_pos.y,size,size))

    def set_color(self,color):
        self.color = color
            
