from pygame.locals import *
from random import randint
import pygame
import time
 
class Apple:
    x = 0
    y = 0
    step = 44
    
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
#changelog: 
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = [0,0]#previosly [0,0]
    length = 3
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length,width,height):
       self.score=0
       limitx=range(44,width-44,44)
       limity=range(44,height-44,44)
       x=limitx[randint(0,len(limitx)-1)]
       y=limity[randint(0,len(limity)-1)]
       random=randint(0,3)
       self.direction=[random,random]
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
       for i in range(length):
          point=[]
          if self.direction[1]==0:
            point=[x+i-44,y]
          if self.direction[1]==1:
            point=[x+i+44,y]
          if self.direction[1]==2:
            point=[x,y+i*44]
          if self.direction[1]==3:
            point=[x,y-i*44]
          self.x[i]=point[0]
          self.y[i]=point[1]
       # initial positions, no collision.
       #self.x[1] = -1*self.step
       #self.x[2] = -2*self.step
 
    def update(self):
        #print("score"+str(self.score))
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction[1] == 0:
              if self.direction[0] != 1:
                self.x[0]=self.right()
              else:
                self.x[0]=self.left()
                  
            elif self.direction[1] == 1:
              if self.direction[0] != 0:
                self.x[0]=self.left() 
              else:
                self.x[0]=self.right()
                
            elif self.direction[1] == 2:
              if self.direction[0] != 3:
                self.y[0]=self.up()
              else:
                self.y[0]=self.down()
                
            else:
              if self.direction[0] != 2:
                self.y[0]=self.down()
              else:
                self.y[0]=self.up()
                
                
            self.updateCount = 0
        
 
    def genericMove(self,action):
        #print("generic move called")
        if action==0:self.moveRight()
        elif action==1:self.moveLeft()
        elif action==2:self.moveUp()
        else:self.moveDown()
        self.update()
    
    def left(self):
      a = self.x[0] - self.step
      return a
    def right(self):
      a = self.x[0] + self.step
      return a
    def up(self):
      a = self.y[0] - self.step
      return a
    def down(self):
      a = self.y[0] + self.step
      return a
        
        
    def moveRight(self):
        #print("right")
        self.direction[0]=self.direction[1]
        self.direction[1] = 0
 
    def moveLeft(self):
        #print("left")
        self.direction[0]=self.direction[1]
        self.direction[1] = 1 
 
    def moveUp(self):
        #print("up")
        self.direction[0]=self.direction[1]
        self.direction[1] = 2
 
    def moveDown(self):
        #print("down")
        self.direction[0]=self.direction[1]
        self.direction[1] = 3
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize,game=None):
        #print(x1,y1,x2,y2)
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
              #print('('+str(x1)+','+str(y1)+'),('+str(x2)+','+str(y2)+')')
              if game:
                game._running=False
              return True
        return False        
    def inLimit(self,x1,y1,x2,y2,bsize,game=None):
      #print(x1,y1,x2,y2)
      if x1 < x2 + bsize or y1 < y2 + bsize or y2<0 or x2<0:
            #print("You lose! Collision: ")
            if game:
              game._running=False
            #print("x[0] (" + str(x1) + "," + str(y1) + ")")
            return True
      return False
    
class App:
 
    windowWidth = 900
    windowHeight = 700
    player = 0
    apple = 0
    objects=[0,0,0]
    
    def reset(self):
      self.__init__()
      self.on_init()
      self.on_render()
      #print(self.player.x[0],self.player.y[0],self.player.length)
    
      
      
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3,self.windowWidth,self.windowHeight) 
        self.apple = Apple(randint(1,19),randint(1,15))
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Snake A.I')
        self._running = True
        self._image_surf = pygame.image.load("block.jpg").convert()
        self._apple_surf = pygame.image.load("block.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def checkAppleEaten(self):
      if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[0], self.player.y[0],44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.player.length = self.player.length + 1
                self.player.score=self.player.score+1
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?
        #for i in range(0,self.player.length):
        self.checkAppleEaten()
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40,self):
                #print("You lose! Collision: ")
                #print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                #print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)
        
        if self.game.inLimit(self.windowWidth, self.windowHeight, self.player.x[0], self.player.y[0], 44, self):
          #print("You lose! Collision: ")
          #print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")") 
          pass
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))#color
        self.player.draw(self._display_surf, self._image_surf)#draw snake 
        self.apple.draw(self._display_surf, self._apple_surf)#draw apple
        pygame.display.flip()#displays full surface
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()#not much significant
            for ev in pygame.event.get():
              if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:  
                  self.player.moveRight()

                elif ev.key == pygame.K_LEFT:
                    self.player.moveLeft()
     
                elif ev.key == pygame.K_UP:
                    self.player.moveUp()
     
                elif ev.key == pygame.K_DOWN:
                    self.player.moveDown()
     
                else:
                    self._running = False
 
            self.on_loop()#on_loop functions continously updates player 
            self.on_render()#on_render continously updates the screen 
 
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    print("yay")