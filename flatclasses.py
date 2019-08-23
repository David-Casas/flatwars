import pygame
from pygame.locals import *
import math

SPEED = 1
TIME = 1
MARGIN = 3
WINH, WINW = 700 +2*MARGIN, 1300 + 2*MARGIN
BTLFLDH, BTLFLDW = 700, 900

BLACK = (0,0,0,0)
GRAY = (150,150,150,0)
DEEPBLUE = (0,4,130,0)
class spaceObject:
    """Clase principal de objeto.
    Atributos:
        pos = (x,y) una tupla de enteros con la posición de la esquina sup izquierda.
        v_x, v_y = Las aceleraciones x e y respectivamente.
    Métodos:
        draw(surf): dibujarse en la superficie."""
    pos = (0,0)
    v_x = 0
    v_y = 0
    time_x = 0
    time_y = 0
    def __init__(self,newPos = None):
        if newPos == None:
            #Siempre iniciará quieto por el momento.
            self.pos = (0,0)
        else:
            self.pos = newPos
    
    
    def getPos(self):
        return self.pos
    def setPos(self,newX, newY):
        self.pos = (newX, newY)
    def getVX(self):
        return self.v_x
    def setVX(self,newVX):
        self.v_x = newVX
    def getVY(self):
        return self.v_y
    def setVY(self,newAY):
        self.v_y = newAY
    def getV(self):
        return (self.v_x,self.v_y)
    def setV(self, newAX, newAY):
        self.v_x,self.v_y = newAX, newAY
    def calcPos(self):
        self.pos = (int(self.pos[0] + (self.v_x)),int(self.pos[1]+(self.v_y)))
    def velUp(self):
        self.v_y = self.v_y -SPEED
    def velDown(self):
        self.v_y = self.v_y + SPEED
    def velRight(self):
        self.v_x = self.v_x +SPEED
    def velLeft(self):
        self.v_x = self.v_x -SPEED
    dictAccs = {pygame.K_UP: velUp, pygame.K_DOWN: velDown, pygame.K_RIGHT: velRight, pygame.K_LEFT: velLeft}

class ship(spaceObject):
    '''Clase nave. Hereda de spaceObject
     '''
    color = (0,0,0,0)
    def __init__(self, newPos =None, newColor = None):
        if newColor == None:
            pass
        else:
            self.color = newColor
        spaceObject.__init__(self,newPos)

    def draw(self, surf, backSurf):
        pygame.draw.circle(surf, self.color, (self.pos), 20)
        backSurf.blit(surf, (MARGIN, MARGIN))
        pygame.display.flip()
