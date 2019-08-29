import pygame
from pygame.locals import *
import math
import flatclasses as fcls
import random    

#TODO: Hacer que cambie de escenario si se sale hacia la derecha.
MARGIN = 3
WINH, WINW = 700 +2*MARGIN, 1300 + 2*MARGIN
BTLFLDH, BTLFLDW = 700, 900
BASEW, BASEH = 50, 100

ALLYBASEX, ALLYBASEY =0,250
ENEMYBASEX, ENEMYBASEY = BTLFLDW-50, 250
ENEMYCOLOR = (255,255,0)
ALLYCOLOR = (0,0,255)
BLACK = (0,0,0,0)
GRAY = (150,150,150,0)
DEEPBLUE = (0,4,130,0)



def clearSurf(surf, backSurf):
    #dibujar las líneas
    surf.fill(BLACK)
    for ypoint in range(int(BTLFLDH/50)):
        pygame.draw.line(surf, GRAY, (0,50*ypoint),(BTLFLDW, 50*ypoint))
    for xpoint in range(int(BTLFLDW/50)):
        pygame.draw.line(surf, GRAY, (50*xpoint,0), (50*xpoint, BTLFLDH))
    
    backSurf.blit(surf, (MARGIN, MARGIN))
    
    pygame.display.flip()
    
    
#Init
pygame.init()
pygame.font.init()

#Crea la ventana base.
mainWindow = pygame.display.set_mode((WINW, WINH))
pygame.display.set_caption('FlatWars')
mainWindow.fill(DEEPBLUE)

#Superficies
#Campo de Batalla
btlfldSurf = pygame.Surface((BTLFLDW, BTLFLDH)).convert()
#Bases
allyBase = fcls.base(ALLYCOLOR, (ALLYBASEX, ALLYBASEY))
enemyBase = fcls.base(ENEMYCOLOR, (ENEMYBASEX, ENEMYBASEY), isEnemy = True)
#Crea las naves
myShip = fcls.ship(newPos = (100,350), newColor =(0,0,255))
ally1 = fcls.nship(newPos = (ALLYBASEX + 100, ALLYBASEY - 100), newColor = ALLYCOLOR)
ally2 = fcls.nship(newPos = (ALLYBASEX +150, ALLYBASEY + 100), newColor = ALLYCOLOR)
enemy1=fcls.nship(newPos = (ENEMYBASEX -100, ENEMYBASEY - 100), newColor = ENEMYCOLOR)
enemy2=fcls.nship(newPos = (ENEMYBASEX -50, ENEMYBASEY + 100), newColor =ENEMYCOLOR)
#Blit todo antes de empezar.
mainWindow.blit(btlfldSurf, (MARGIN, MARGIN))
pygame.display.flip()

#Dibujar Superficie.
clock = pygame.time.Clock()
def main():
    #Mainloop.
    keep = True
    frame = 0
    while keep:
        
        toDraw = []
        clearSurf(btlfldSurf, mainWindow)#Limpia la superficie.
        #Dibuja todos los objetos
        for thing in fcls.inGame:
            toDraw.append(thing.draw(btlfldSurf))
        mainWindow.blit(btlfldSurf, (MARGIN, MARGIN))
        pygame.display.update(toDraw)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in list(myShip.dictAccs.keys()):
                    if event.key == pygame.K_w:
                        myShip.velUp(1)
                    elif event.key == pygame.K_s:
                        myShip.velDown(1)
                    elif event.key == pygame.K_d:
                        myShip.velRight(1)
                    elif event.key == pygame.K_a:
                        myShip.velLeft(1)
                elif event.key ==pygame.K_SPACE:
                    myShip.misil(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                myShip.shot(pygame.mouse.get_pos())
        clock.tick(60)
        frame = frame +1
    pygame.quit()

if __name__ == "__main__":
    main()
