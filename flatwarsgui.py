import pygame
from pygame.locals import *
import math
import flatclasses as fcls
import random    

#TODO: Hacer que cambie de escenario si se sale hacia la derecha.
#TODO: Mejorar puntería
#TODO: Condiciones de victoria y perdida.
#TODO: Carteles que indiquen la velocidad.
#TODO: Que las naves se eviten.
#TODO: Que un misil destruya naves a la redonda.

MARGIN = 3
WINH, WINW = 700 +2*MARGIN, 1300 + 2*MARGIN
BTLFLDH, BTLFLDW = 700, 900
BASEW, BASEH = 50, 100

ALLIES = 30
ENEMIES = 30

ALLYBASEX, ALLYBASEY =0,300
ENEMYBASEX, ENEMYBASEY = BTLFLDW-50, 250
ENEMYCOLOR = (255,255,0)
ALLYCOLOR = (0,0,255)
SELFCOLOR = (100,100,255)
BLACK = (0,0,0,0)
GRAY = (150,150,150,0)
DEEPBLUE = (0,4,130,0)
SHIRAD = 20
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
allyBase = fcls.base(ALLYCOLOR, (ALLYBASEX, ALLYBASEY), team = 1)
enemyBase = fcls.base(ENEMYCOLOR, (ENEMYBASEX, ENEMYBASEY), isEnemy = True, team = 2)
#Crea las naves
myShip = fcls.ship(newPos = (150,350), newColor =SELFCOLOR, team = 1)
Team1 =[myShip,
fcls.nship(newPos = (ALLYBASEX + 100, ALLYBASEY- 200), newColor = ALLYCOLOR, team = 1),
fcls.nship(newPos = (ALLYBASEX + 100, ALLYBASEY + 200), newColor = ALLYCOLOR, team = 1),
fcls.nship(newPos= (ALLYBASEX + 200, ALLYBASEY  - 200), newColor = ALLYCOLOR, newBehav = 2, team = 1),
fcls.nship(newPos= (ALLYBASEX + 200, ALLYBASEY + 300), newColor = ALLYCOLOR, newBehav = 2, team = 1)]

Team2 =[fcls.nship(newPos = (ENEMYBASEX -100, ENEMYBASEY - 200), newColor = ENEMYCOLOR, team = 2),
fcls.nship(newPos = (ENEMYBASEX -100, ENEMYBASEY + 400), newColor =ENEMYCOLOR, team = 2),
fcls.nship(newPos= (ENEMYBASEX -150 , ENEMYBASEY + 50), newColor = ENEMYCOLOR, newBehav = 2, team = 2),
fcls.nship(newPos= (ENEMYBASEX -200, ENEMYBASEY -200), newColor = ENEMYCOLOR, newBehav = 2, team = 2),
fcls.nship(newPos = (ENEMYBASEX -200, ENEMYBASEY +300), newColor = ENEMYCOLOR, newBehav = 2, team = 2)]

#Blit todo antes de empezar.
mainWindow.blit(btlfldSurf, (MARGIN, MARGIN))
pygame.display.flip()
#Dibujar Superficie.
clock = pygame.time.Clock()



def clearSurf(surf, backSurf):
    #dibujar las líneas
    surf.fill(BLACK)
    for ypoint in range(int(BTLFLDH/50)):
        pygame.draw.line(surf, GRAY, (0,50*ypoint),(BTLFLDW, 50*ypoint))
    for xpoint in range(int(BTLFLDW/50)):
        pygame.draw.line(surf, GRAY, (50*xpoint,0), (50*xpoint, BTLFLDH))
    
    backSurf.blit(surf, (MARGIN, MARGIN))
    
    pygame.display.flip()
    
    

def main():
    global myShip, ENEMIES, ALLIES
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
        #Quitar las naves que no están el el juego
        for team in [Team1, Team2]:
            for ship in team:
                if not(ship in fcls.inGame):
                    team.remove(ship)
        #Rellenar los equipos dada una perdida.
        #Ver si el prota murió
        if not(myShip in Team1):
            myShip = fcls.ship(newPos = (150,350), newColor = SELFCOLOR, team = 1)
            Team1.append(myShip)
        if len(Team1) < 5 and ALLIES > 0:
            ALLIES -= 1
            Team1.append(fcls.nship(newPos = (random.randrange(ALLYBASEX +100 ,ALLYBASEX + 150, 2*SHIRAD),random.randrange(0,BTLFLDH, 2*SHIRAD) ), newColor = ALLYCOLOR, newBehav = random.choice([1,2]), team = 1))
        if len(Team2) <5 and ENEMIES  > 0:
            ENEMIES -= 1
            Team2.append(fcls.nship(newPos = (random.randrange(ENEMYBASEX - 150, ENEMYBASEX - 100, 2*SHIRAD), random.randrange(0, BTLFLDH, 2*SHIRAD)), newColor = ENEMYCOLOR, newBehav = random.choice([1,2]), team = 2))
        clock.tick(60)
        frame = frame +1
    pygame.quit()

if __name__ == "__main__":
    main()
