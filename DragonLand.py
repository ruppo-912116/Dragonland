import pygame
from pygame.locals import*
import time
import random


#set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
pygame.display.set_caption('DragonLand')
FPS = 40

pygame.init()
mainClock = pygame.time.Clock()


#set up the colors
BLACK =(0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

moveLeft = False
moveRight = False
moveUp = False
moveDown = False

playerImg = pygame.image.load('shooter.png')
playerRect = playerImg.get_rect()
enemyImg = pygame.image.load('dragon.png')
enemyRect = enemyImg.get_rect()
background = pygame.image.load('background.jpg')
background1 = pygame.transform.scale(background,(800,600))
arrowImg = pygame.image.load('arrow.png')
arrowRect = arrowImg.get_rect()

moveSpeed = 5
enemycount = 40
enemy = []
arrows = []

coll=False

font = pygame.font.SysFont(None,48)
font1 = pygame.font.SysFont(None,24)


def surfaceo(surface):
    surface.blit(background1,(0,0))
    

def drawText(text,font,surface,x,y):
    
    textobj = font.render(text,1,BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)
    pygame.display.update()
    time.sleep(2)

def collisiontest(p,b):
         if p.colliderect(b['rect']):
            return True
         return False
 

def waitforkeypress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_RETURN:
                    return
                
                    
                    
                

def scoredisplay(score):
    text = font1.render("Score: "+str(score),True,BLACK)
    windowSurface.blit(text,(0,0))

def lives(life):
    text = font1.render("Lives: "+str(life),True,BLACK)
    windowSurface.blit(text,(0,15))
   
       

x = 0;
for i in range(8):
    newEnemy ={'rect': pygame.Rect(720,x,80,60),'speed': random.randint(1,8)}
    enemy.append(newEnemy)
    x = x+70

score = 0
addnewenemy = 0
life = 1
flag = 0
start = True
gameLoop = True
i=0

move=False
    
bull=[]
keyspace=True
while gameLoop:
    

    while start == True:

        surfaceo(windowSurface)
        drawText('A simple 2D game',font,windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/3)+40)
        drawText('Rupan Inc.',font,windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/3)+70)
        drawText('Press ENTER..',font,windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/3)+200)
        waitforkeypress()
        start = False

    #filling canvas with the white background
    windowSurface.fill(WHITE)
    
    
        

    #acquiring the event when the key is being pressed
    keys = pygame.key.get_pressed()
    
    #getting the event when the user hit the escape key or exits the filled canvas
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == K_SPACE :
                move=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()   
                    
                
                
    #Restricting the movement of the player so it doesnot go out of the screen and giving agility to the main character
    if keys[pygame.K_UP]:
        if playerRect.top > 0:
            playerRect.top -= moveSpeed
    if keys[pygame.K_DOWN]:
        if playerRect.bottom < WINDOWHEIGHT:
            playerRect.top += moveSpeed
    if keys[pygame.K_SPACE] and keyspace==True:
       x=playerRect.right-15
       y=(playerRect.top+playerRect.bottom)/2-10
       move=True
       i=0
       keyspace=False
       newEnemy ={'rect': pygame.Rect(x,y,20,20),'speed':5}
       bull.append(newEnemy)
       


    i+=1
    if(i>10):
        keyspace=True
        i=0
       
       
       
            
    #drawing player
    windowSurface.blit(playerImg,playerRect)
    
            
    #adding enemies after certain number of loops
    if addnewenemy == enemycount:
        addnewenemy = 0
        newEnemy ={'rect': pygame.Rect(720,random.randint(0,540),80,60),'speed': random.randint(1,4)}
        enemy.append(newEnemy)

        
        
    #deleting the enemies when they reach the end of the screen
    for b in enemy[:]:
        if b['rect'].left <-2:
            flag+=1
            enemy.remove(b)
            
            

    #detecting the collision between player and dragon
    for b in enemy:
       
         
        if collisiontest(playerRect,b):
            life-=1
            
            enemy.remove(b)
            coll=False

    #bullet and dragon collision
    for bulls in bull:
        for enemys in enemy:
            if collisiontest(bulls['rect'],enemys):
                score+=1
                enemy.remove(enemys)
                bull.remove(bulls)

        #bullet removing after leaving screen
        if bulls['rect'].right>700:
            bull.remove(bulls)


    
    

            
    if flag == 3:
        life -= 1
        flag = 0

    scoredisplay(score)
    lives(life)

    #game over screen
    if life == 0:
        windowSurface.fill(WHITE)
        text = font.render("GAME OVER!!!",True,BLACK)
        text1 = font.render("Press C to continue and ESC to exit the game",True,BLACK)
        windowSurface.blit(text,(300,200))
        windowSurface.blit(text1,(100,300))
        pygame.display.update()
        waitforkeypress()
        
        
    
    #drawing enemies
    for b in enemy:
        b['rect'].move_ip(-b['speed'],0)
        windowSurface.blit(enemyImg,b['rect'])

 
    for b in bull:
         b['rect'].move_ip(+b['speed'],0)
         windowSurface.blit(arrowImg,b['rect'])
        
        

    mainClock.tick(FPS)
    addnewenemy += 1
    pygame.display.update()
            
                





