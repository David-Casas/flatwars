import pygame
from pygame.locals import *
import math


SPEED = 1
TIME = 1
MARGIN = 3
WINH, WINW = 700 +2*MARGIN, 1300 + 2*MARGIN
BTLFLDH, BTLFLDW = 700, 900
SHIRAD = 20
CANNW, CANNH = 12,24

BLACK = (0,0,0,0)
GRAY = (150,150,150,0)
DEEPBLUE = (0,4,130,0)

objectsToDraw = []

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
    dictAccs = {pygame.K_w: velUp, pygame.K_s: velDown, pygame.K_d: velRight, pygame.K_a: velLeft}

class bullet(spaceObject):
    '''Clase para un projectil. '''
    vel = 0
    objtv= (0,0)
    def __init__(self, newPos = None, newVel = None, newObjtv =None):
        if newVel==None:
          pass
        else:
            self.vel = newVel
        if newObjtv==None:
          pass
        else:
            self.objtv = newObjtv
            
        spaceObject.__init__(self,newPos)
        
        objtvx, objtvy =newObjtv[0], newObjtv[1]
        px, py = self.pos[0], self.pos[1]
        dis = math.sqrt((objtvx - px)**2+(objtvy - py)**2)
        cosA, sinA = (objtvx - px)/dis, (objtvy - py)/dis
        
        self.setV(self.vel*cosA,self.vel*sinA)
        
    def draw(self, surf, backSurf):
        pygame.draw.circle(surf, (255,255,255), self.pos, 3)
        backSurf.blit(surf, (MARGIN, MARGIN))
        pygame.display.flip()
        
class ship(spaceObject):
    '''Clase nave. Hereda de spaceObject
     '''
    color = (0,0,0,0)
    cannRect = ((0,0), (0,0))
    def __init__(self, newPos = None, newColor = None):
        if newColor == None:
            pass
        else:
            self.color = newColor
        
        spaceObject.__init__(self,newPos)
        
        


    def update(self):
        mpx, mpy = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]#Not clean
        posx, posy = self.pos[0], self.pos[1]
        dis = math.sqrt((mpx - posx)**2 + (mpy - posy)**2)
        sinA = (mpy -posy)/dis
        cosA = (mpx - posx)/dis
        return (int(posx +SHIRAD*cosA),int( posy + SHIRAD*sinA))
    
    def draw(self, surf, backSurf):
        pygame.draw.circle(surf, self.color, self.pos, SHIRAD)
        pygame.draw.circle(surf, (255,255,255,0), self.update(), int(SHIRAD/4))
        backSurf.blit(surf, (MARGIN, MARGIN))
        pygame.display.flip()
        
    def shot(self):
        objectsToDraw.append(bullet(newPos = self.update(), newVel = 5 , newObjtv = pygame.mouse.get_pos()))
        
