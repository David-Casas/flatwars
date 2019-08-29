import pygame
from pygame.locals import *
import math
import random
import numpy
import pygame.surfarray


SPEED = 1
TIME = 1
MARGIN = 3
WINH, WINW = 700 +2*MARGIN, 1300 + 2*MARGIN
BTLFLDH, BTLFLDW = 700, 900
BASEW, BASEH = 50, 200
SHIRAD = 20
SHIPW, SHIPH = 2*SHIRAD,2*SHIRAD
BULLETRAD = 3
MISILRAD = 10
CANNW, CANNH = 12,24
SHIP_SOURCE = 'resources/ship.png'
MISIL_SOURCE = 'resources/misil.png'

RANGE = 100

BLACK = (0,0,0,0)
GRAY = (150,150,150,0)
DEEPBLUE = (0,4,130,0)
#Jugada arriesgada y no muy pythonica para establecer ids para cada uno.
inGame = []

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
    def __init__(self,newPos = None):
        if newPos == None:
            #Siempre iniciará quieto por el momento.
            self.pos = (0,0)
        else:
            self.pos = newPos
        self.id = (self.pos[0] +random.randint(1, RANGE) ,self.pos[1] + random.randint(1,RANGE))
        self.rect = ((0,0),(0,0))
        self.shooted = False
        self.posX = self.pos[0]
        self.posY = self.pos[1]
    #Definir igualdad.
    def __eq__(self, other):
        return self.id == other.id
    def __ne__(self, other):#Recomiendan definir esto también.
        return self.id != other.id
    def getX(self):
        return self.posX
    def setX(self, newX):
        self.posX = newX
    def getY(self):
        return self.posY
    def setX(self, newX):
        self.posY = newY
    def getPos(self):
        return (self.posX, self.posY)
    def setPos(self,newX, newY):
        self.posX, self.posY = newX, newY
    def getVX(self):
        return self.v_x
    def setVX(self,newVX):
        if self.shooted:#Si le han disparado no puede cambiar.
            pass
        else:
            self.v_x = newVX
    def getVY(self):
        return self.v_y
    def setVY(self,newAY):
        if self.shooted:#Si le han disparado no puede cambiar.
            pass
        else:
            self.v_y = newAY
    def getV(self):
        return (self.v_x,self.v_y)
    def setV(self, newAX, newAY):
        if self.shooted:
            pass
        else:
            self.v_x,self.v_y = newAX, newAY
    def getRect(self):
        return pygame.Rect(self.rect)
    def setRect(self, newRect):
        self.rect = pygame.Rect(newRect)    
    def calcPos(self):
        self.posX, self.posY = int(self.posX + (self.v_x)),int(self.posY+(self.v_y))
    def velUp(self, speed):
        if self.shooted:
            pass
        else:
            self.v_y = self.v_y - speed
    def velDown(self, speed):
        if self.shooted:
            pass
        else:
            self.v_y = self.v_y + speed
    def velRight(self, speed):
        if self.shooted:
            pass
        else:
            self.v_x = self.v_x + speed
    def velLeft(self, speed):
        if self.shooted:
            pass
        else:
            self.v_x = self.v_x - speed
    def switchShooted(self):
        #print('Impacto!!')
        self.shooted = not self.shooted
    def getShooted(self):
        return self.shooted
        
    def isOut(self):
        if not(0 <= self.posX <= BTLFLDW) or not(0<= self.posY <= BTLFLDH):
            inGame.remove(self)
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
        
    def draw(self, surf):
        self.calcPos()
        self.setRect(pygame.draw.circle(surf, (255,255,255), self.getPos(), BULLETRAD))
        self.isOut()
        return self.getRect()

class misil( bullet, pygame.sprite.Sprite):
    """Clase misil para destruir la nave."""
    def __init__(self, newPos = None, newVel = None, newObjtv =None):
        bullet.__init__(self,newPos, newVel, newObjtv)
        self.image = pygame.transform.scale(pygame.image.load(MISIL_SOURCE).convert_alpha(), (MISILRAD*2, MISILRAD*2))
        
        
    def update(self):
        if self.getShooted():
            return   
        for thing in inGame:
            if self.getRect().colliderect(thing.getRect()) and self != thing:
                self.switchShooted()
                inGame.remove(self)
                if type(thing) is base:
                    print('Impacto base')
            
    def draw(self, surf):
        self.update()
        if self.getShooted():
            surf.blit(self.image, self.getPos())
            self.setRect((self.getPos(), (MISILRAD*2, MISILRAD*2)))
            self.isOut()
            return self.getRect()
        else:
            self.calcPos()
            surf.blit(self.image, self.getPos())
            self.setRect((self.getPos(), (MISILRAD*2, MISILRAD*2)))
            self.isOut()
            return self.getRect()
        
class ship(spaceObject, pygame.sprite.Sprite):
    '''Clase nave. Hereda de spaceObject
     '''
    def __init__(self, newPos = None, newColor = None):
        super().__init__()
        self.hasMisil = True
        self.pos = newPos
        self.color = newColor        
        spaceObject.__init__(self,newPos)
        self.setRect((self.getX(), self.getY(), SHIPW, SHIPH))
        self.image = pygame.image.load(SHIP_SOURCE).convert_alpha()
        self.pixArr =  pygame.surfarray.pixels3d(self.image)
        #Cambiar para el color
        for xcor in range(len(self.pixArr[1])):#Recorre las filas.
            for ycor in range(len(self.pixArr[2])):#Columnas
                if (self.pixArr[xcor][ycor] == [255,255,255]).all():#Si es blanco le cambia al color.
                    self.pixArr[xcor][ycor] = self.color
                elif (self.pixArr[xcor][ycor] == [0,0,0]).all():
                    self.pixArr[xcor][ycor] = [0,255,0]
                #print(self.pixArr[xcor][ycor] == [255,255,255])
        del self.pixArr
        inGame.append(self)
        
    def update(self, objective):#Son las coordenadas donde debe apuntar.
        
        mpx, mpy = objective[0],objective[1]#Not clean
        posx, posy = self.getRect().centerx, self.getRect().centery
        dis = math.sqrt((mpx - posx)**2 + (mpy - posy)**2)
        sinA = (mpy -posy)/dis
        cosA = (mpx - posx)/dis
        
        
        return (int(posx + 2*SHIRAD*cosA),int( posy + 2*SHIRAD*sinA))
    
    def collided(self):
        #Va a ver si ha chocado con algo
        toCheck = [x.getRect() for x in inGame if not(x == self)]
        colided = self.getRect().collidelist(toCheck)
        if colided != -1 and not self.getShooted():
            self.switchShooted()
        
    
    def draw(self, backSurf):
        self.collided()
        self.calcPos()
        backSurf.blit(self.image, (self.getPos()))
        self.setRect((self.getPos(),(SHIPW,SHIPH)))
        self.isOut()
        return self.getRect()
        
    def shot(self, objective):
        inGame.append(bullet(newPos = self.update(objective), newVel = 10 , newObjtv = objective))
    def misil(self, objective):
        if self.hasMisil:
            inGame.append(misil(newPos = self.update(objective), newVel = 3, newObjtv = objective))
            pixArr =  pygame.surfarray.pixels3d(self.image)
            #Cambiar para el color
            for xcor in range(len(pixArr[1])):#Recorre las filas.
                for ycor in range(len(pixArr[2])):#Columnas
                    if (pixArr[xcor][ycor] == [0,255,0]).all():#Si es negro le cambia al color.
                        pixArr[xcor][ycor] = [255,0,0]
            del pixArr
            self.hasMisil = False
        else:
            pass




class nship(ship):
    """Clase para nave enemiga. """
    
    def __init__(self, newPos = None, newColor = None, newBehav =1):
        ship.__init__(self, newPos, newColor)
        self.origin = newPos #Guardar donde nació.
        self.Behav = newBehav
        self.setVY(0)
        
    def guardian(self):
        #Si está quieto lo mueve a algún lado.
        if self.getVY() == 0:
            newVel = random.choice([1,-1])
            self.setVY(newVel)               
        #Va a ir de arriba a abajo.
        if(math.fabs(self.getY() - self.origin[1])>= 50):
            self.setVY(-1*self.getVY())
        #Revisar todas las cosas que están al rededor unos __ pixeles a la redonda y si son misiles o naves enemigas.
        for thing in inGame:
            if (math.sqrt((thing.getX() - self.getX())**2 + (thing.getY() - self.getY())**2 ) <=100 and
                (type(thing) is misil or 
                ((type(thing) is ship or type(thing) is nship) and thing.color != self.color)) ):
                self.shot(thing.getPos())
    #Este tipo de nave 
    #def killer(self):
        
            
    dictBehav ={1: guardian }
    def draw(self, backSurf):
        self.collided()
        self.dictBehav[self.Behav](self)
        self.calcPos()
        backSurf.blit(self.image, (self.getPos()))
        self.setRect((self.getPos(),(SHIPW,SHIPH)))
        self.isOut()
        return self.getRect()
        

        
class base(pygame.sprite.Sprite, spaceObject):
    """Clase para la base de las naves"""
    
    def __init__(self, color, coordenadas, isEnemy = False):
        super().__init__()
        spaceObject.__init__(self,coordenadas)
        self.image = pygame.Surface((BASEW, BASEH)).convert()
        self.color = color
        self.image.fill(self.color)
        inGame.append(self)
        self.isEnemy = isEnemy
        

    def getRect(self):
        return pygame.Rect(self.rect)
        
    def draw(self, backSurf):
        self.rect = backSurf.blit(self.image, (self.getX(),self.getY()))
        return self.rect
        
         
