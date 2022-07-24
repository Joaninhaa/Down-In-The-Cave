import pygame
from random import choice
pygame.init()
pygame.font.init()


#Const
WHITE = (255, 244, 200)
BLACK = (24, 20, 37)
PINK = (255, 0, 68)
GREEN = (99, 199, 77)
BLUE = (0, 149, 233)
RED = (228, 59, 68)
COLORS = [WHITE, BLACK, PINK, GREEN, BLUE, RED]

FPS = 60
TAM = 16
RES = [50*TAM, 40*TAM]


#Class
class Player():
    def __init__(self, x, y):
        self.x =x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, TAM, TAM)
        self.testCollision = False
        
        self.hspd = 0
        self.vspd = 0
        self.vel = 5
    
    def draw(self, surf):
        pygame.draw.rect(surf, PINK, self.rect)

    def move(self, keys, tiles):
        '''movement and collision'''
        if self.testCollision:
            hMove = keys[pygame.K_d] - keys[pygame.K_a]
            vMove = keys[pygame.K_s] - keys[pygame.K_w]
            self.hspd = self.vel * hMove
            self.vspd = self.vel * vMove

            #Horizontal movement and collision
            self.rect.x += self.hspd
            for tile in tiles:
                if self.rect.colliderect(tile):
                    if self.hspd > 0:
                        self.rect.x = tile.x - TAM
                    elif self.hspd < 0:
                        self.rect.x = tile.x + TAM
            self.x = self.rect.x

            #Vertical movement and collision
            self.rect.y += self.vspd
            for tile in tiles:
                if self.rect.colliderect(tile):
                    if self.vspd > 0:
                        self.rect.y = tile.y - TAM
                    elif self.vspd < 0:
                        self.rect.y = tile.y + TAM
            self.y = self.rect.y
    
class Manager():
    def __init__(self, steps=600, scale=5):
        self.dirs = ['l', 'r', 'u', 'd'] #left, right, up, down
        self.tiles = []
        self.steps = steps
        self.x = RES[0]//2
        self.y = RES[1]//2
        self.scale = scale
        self.rect = pygame.Rect(self.x, self.y, TAM*self.scale, TAM*self.scale)

    def createCave(self, player):
        player.testCollision = False
        self.tiles = []
        self.x = RES[0]//2
        self.y = RES[1]//2
        self.rect.x = self.x
        self.rect.y = self.y
        #Fill the room with gray blocks
        for y in range(RES[1]//TAM):
            for x in range(RES[0]//TAM):
                a = pygame.Rect(x*TAM, y*TAM, TAM, TAM)
                self.tiles.append(a)
        
        #Move a invisible block around the room and delete the grays blocks that collide with it
        for i in range(self.steps):
            dir = choice(self.dirs)
            x = self.rect.x
            y = self.rect.y
            if dir == 'l' and self.rect.x - TAM > 0:
                self.rect.x -= TAM
            elif dir == 'r' and self.rect.x + TAM < RES[0]-TAM*self.scale:
                self.rect.x += TAM
            elif dir == 'u' and self.rect.y - TAM > 0:
                self.rect.y -= TAM
            elif dir == 'd' and self.rect.y + TAM < RES[1]-TAM*self.scale:
                self.rect.y += TAM        
            self.x = self.rect.x
            self.y = self.rect.y
            if self.rect.collidepoint(self.x, self.y):
                for tile in self.tiles:
                    if self.rect.colliderect(tile):
                        self.tiles.remove(tile)
        
        #set the player position on the room
        player.rect.y = 0
        player.rect.x = 0
        player.y = player.rect.y
        player.x = player.rect.x
        for tile in self.tiles:
            if player.rect.colliderect(tile):
                if player.rect.x < RES[0] -TAM and player.rect.y < RES[1]-TAM:
                    player.rect.x += TAM
                    player.x = player.rect.x
                else:
                    player.rect.y += TAM
                    player.rect.x = 0
                    player.y = player.rect.y
                    player.x = player.rect.x
        player.testCollision = True
        return self.tiles
                    
    def drawCave(self, surf):
        if len(self.tiles) > 0:
            for tile in self.tiles:
                pygame.draw.rect(surf, (50, 50, 50), tile)


#Def
def debug(surf, font, clock):
    #Fps
    txtFps = font.render(str(int(clock.get_fps())), 1, WHITE)
    surf.blit(txtFps, (RES[0]-txtFps.get_width(), 0))

def main():
    '''Main Loop'''
    #Obj
    win = pygame.display.set_mode((RES[0], RES[1]))
    clock = pygame.time.Clock()
    myFont = pygame.font.SysFont('Comic Sans MS', TAM)
    manager = Manager()
    player = Player(0, 0)

    #Vars
    run = True
    tiles = []

    while run:
        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_r:
                    tiles = manager.createCave(player)
        keys = pygame.key.get_pressed()        
        player.move(keys, tiles)

        #graphics
        win.fill(BLACK)
        manager.drawCave(win)
        player.draw(win)
        debug(win, myFont, clock)
        pygame.display.update()

        clock.tick(FPS)


main()