from errno import WSAEDESTADDRREQ
import os
from tkinter import W
import pygame
import pygame.freetype
import random as rand

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BlockGame')
pygame.font.init()
my_font = pygame.freetype.Font('Mont.otf', 30)

hs = ''
if(os.path.exists("highscore.txt")):
    f = open("highscore.txt", 'r+')
else:
    open("highscore.txt", 'w+')
    f = open("highscore.txt", 'r+')
hs = f.read()
if(not hs):
    hs = 0
elif(not hs.isnumeric()):
    print("Something is wrong with highscore file, creating a new one")
    f = open("highscore.txt", 'w')
    f.write('0')
    hs = 0
hs= int(hs)

block = pygame.Rect((0, 0, 0, 0))
blockrect = pygame.Rect((0, 0, 0, 0))
sizebtwn = 50
blockSize = 50
isClicked = False
fullRow = True
fullColumn = True
emptyMap = True
score = 0

map = [[0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],
       [0, 0, 0, 0, 0, 0, 0, 0 ,0],]

class blockClass:
    def __init__(self, formationx, formationy): 
        self.formationx = formationx
        self.formationy = formationy

blocks = [blockClass([0, 0, 0, 0 ], [-2, -1, 0, 1]), #long1
          blockClass([2, 1, 0, -1], [0, 0, 0, 0]),#long2
          blockClass([1, 0, -1], [0, 0, 0]), #long3
          blockClass([0, 0, 0], [-1, 0, 1]), #long4
          blockClass([0, 0], [0, 1]), #short1
          blockClass([0, 1], [0, 0]), #short2
          blockClass([0, 0, 0, 1], [-1, 0, 1, 1]),#l1
          blockClass([1, 1, 0, -1], [-1, 0 , 0 ,0]),#l2
          blockClass([-1, 0, 1, 1], [0, 0, 0, -1]),#l3
          blockClass([1, 0, 0, 0], [-1, -1, 0, 1]),#l4
          blockClass([0, 1, 0 ,1], [-1, -1, 0, 0]),#square
          blockClass([-1, 0, 1, 0], [1,1 ,1 ,0]),#plus
          blockClass([-1, 0, 0, 1], [1, 1, 0 ,0]),#z1
          blockClass([-1, 0, 0, 1], [0, 0, 1, 1])#z2
    ]


rectangles = []

def drawGrid():
    for x in range(300, 700, blockSize):
        for y in range(150, 550, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            
def drawCurrentBlock(block):
    i = 0
    for x in block.formationx:
        
        if(not isClicked):
            blockrect = pygame.Rect(475 + block.formationx[i] * blockSize, 750 + block.formationy[i] * blockSize, blockSize, blockSize)
            pygame.draw.rect(screen, (255, 255, 255), blockrect)
        x, y = pygame.mouse.get_pos()
        if(isClicked):
            blockrect = pygame.Rect(x + block.formationx[i] * blockSize - 25, y + block.formationy[i] * blockSize -25, blockSize, blockSize)
            pygame.draw.rect(screen, (255, 255, 255), blockrect)
        i = i + 1
        
def drawButton():
    my_font.render_to(screen, (737, 712), f"Reset", (255, 255, 255))
    buttonRect = pygame.Rect(725, 700, 100, 50)
    pygame.draw.rect(screen, (255, 255, 255), buttonRect, 1)
    
def reset():
    for j in range(8):
        for k in range(8):
            map[j][k] = 0
           
def drawBox():
    box = pygame.Rect(375, 600, 250, 250)
    pygame.draw.rect(screen, (255, 255, 255), box, 1)

currentRect = blocks[rand.randint(0, len(blocks)-1)]
run = True
while run:
    
    screen.fill((0, 0, 0))
    my_font.render_to(screen, (40, 350), f"Score: {score}", (255, 255, 255))
    my_font.render_to(screen, (40, 375), f"High Score: {hs}", (255, 255, 255))
    if(score > hs): hs = score
    drawGrid()
    drawButton()
    drawBox()
    drawCurrentBlock(currentRect)
    for j in range(8):
        for k in range(8):
            if (map[k][j]):
                rect = pygame.Rect( 300 + j * blockSize, 150 + k * blockSize, blockSize, blockSize)
                pygame.draw.rect(screen, (255, 255, 255), rect)
    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            if(x > 375 and x < 625 and y > 600 and y < 850):
                isClicked = True
            if(x > 725 and x < 825 and y > 700 and y < 750):
                reset()
                score = 0
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and isClicked:
            isClicked = False
            x, y = pygame.mouse.get_pos()
            ok = True
            
            if(x > 300 and x < 700 and y > 150 and y < 550):
                i = 0
                for z in currentRect.formationx:
                    ix = (x + currentRect.formationx[i] * blockSize) // sizebtwn - 6
                    iy = (y + currentRect.formationy[i] * blockSize) // sizebtwn - 3
                
                    if(ix > 7 or iy > 7 or ix < 0 or iy < 0):
                        ok = False
                        break
                    if(map[iy][ix]):
                        ok = False
                    i = i+1
                
                if(ok):
                    i = 0
                    for z in currentRect.formationx:
                        ix = (x + currentRect.formationx[i] * blockSize) // sizebtwn 
                        iy = (y + currentRect.formationy[i] * blockSize) // sizebtwn
                        block = pygame.Rect((ix*sizebtwn, iy*sizebtwn, 50, 50))
                        map[iy-3][ix-6] = 1
                        for j in range(8):
                            fullColumn = True
                            for k in range(8):
                                if(not map[k][j]):
                                    fullColumn = False
                            if(fullColumn):
                                score = score + 50
                                for k in range(8):
                                    map[k][j]=0
                        for j in range(8):
                            fullRow = True
                            
                            for k in range(8):
                                if(not map[j][k]):
                                    fullRow = False
                            if(fullRow):
                                score = score + 50
                                for k in range(8):
                                    map[j][k]=0
                        emptyMap = True
                        for j in range(8):
                            for k in range(8):
                                if(map[k][j]):
                                    emptyMap = False
                        if (emptyMap and score > 300): score += 300
                        i = i + 1
                    currentRect = blocks[rand.randint(0, len(blocks)-1)]
            
            
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()        
    pygame.display.update()
            
pygame.quit()

f = open("highscore.txt", "w")
f.write(str(hs))

