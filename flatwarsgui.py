import pygame
from pygame.locals import *
import math
import flatclasses as fcls
    


MARGIN = 3
WINH, WINW = 700 +2*MARGIN, 1300 + 2*MARGIN
BTLFLDH, BTLFLDW = 700, 900

BLACK = (0,0,0,0)
GRAY = (150,150,150,0)
DEEPBLUE = (0,4,130,0)



def clearSurf(surf):
    #dibujar las líneas
    surf.fill(BLACK)
    for ypoint in range(int(BTLFLDH/50)):
        pygame.draw.line(surf, GRAY, (0,50*ypoint),(BTLFLDW, 50*ypoint))
    for xpoint in range(int(BTLFLDW/25)):
        pygame.draw.line(surf, GRAY, (50*xpoint,0), (50*xpoint, BTLFLDH))
    
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
btlfldSurf.fill(BLACK)


myShip = fcls.ship(newPos = (350,450), newColor =(255,0,0,0))
fcls.objectsToDraw.append(myShip)
mainWindow.blit(btlfldSurf, (MARGIN, MARGIN))
pygame.display.flip()


#Dibujar Superficie.
clock = pygame.time.Clock()
def main():
    #Mainloop.
    keep = True
    frame = 0
    while keep:
        clearSurf(btlfldSurf)
        for thing in fcls.objectsToDraw:
            if not(0<=thing.getPos()[0]<= BTLFLDW)or not(0<=thing.getPos()[1]<= BTLFLDH):
                fcls.objectsToDraw.remove(thing)
                continue 
            thing.calcPos()
            thing.draw(btlfldSurf, mainWindow)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in list(myShip.dictAccs.keys()):
                    if event.key == pygame.K_w:
                        #print('Arriba')
                        myShip.velUp()
                    elif event.key == pygame.K_s:
                        #print('Abajo')
                        myShip.velDown()
                    elif event.key == pygame.K_d:
                        #print('Derecha')
                        myShip.velRight()
                    elif event.key == pygame.K_a:
                        #print('Izquierda')
                        myShip.velLeft()
            if event.type == pygame.MOUSEBUTTONDOWN:
                myShip.shot()
        clock.tick(60)
        frame = frame +1
    pygame.quit()

if __name__ == "__main__":
    main()
