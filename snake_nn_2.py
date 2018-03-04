# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 21:58:09 2018

@author: bmitra


neural network training for snake to learn how to play
"""

import main
import numpy as np
from random import randint
import time
import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy.linalg as la
import math

class snake:
  def __init__(self,initial_games =1000, test_games = 150, goal_steps = 200):
    self.directions=[
        [[0,-1],2],
        [[1,1],2],
        [[0,1],3],
        [[1,-1],3],
        [[3,1],1],
        [[2,-1],1],
        [[2,1],0],
        [[3,-1],0]
        ]
    self.goalSteps=goal_steps
    self.testGames=test_games
    self.initialGames=initial_games
  
  def automatedMovesForSnake(self):

    training_data=[]
    self.theApp=main.App()
    for _ in range(self.initialGames):
      self.theApp.reset()
      obs=self.generate_observation()
      prev_distance=self.getAppleDistance()
      prev_score=self.theApp.player.score
      for _ in range(self.goalSteps):
        #print(obs)
        #print("snake direction" + str(self.theApp.player.direction))
        #print("snake pos: %d, %d apple position: %d, %d"%(self.theApp.player.x[0],self.theApp.player.y[0],self.theApp.apple.x,self.theApp.apple.y))
        
        new_action,direction=self.action()
        #print("new_Action"+str(new_action))
        self.makeMoveAndCheckCollision(direction)
        new_distance=self.getAppleDistance()
        #print("(prev_distance,new_distance) (%f,%f)"%(prev_distance,new_distance))
        new_score=self.theApp.player.score
        
        if not self.theApp._running:
          #print(self.theApp.player.x[0],self.theApp.player.y[0])
          training_data.append([self.add_action_to_observation(obs, float(new_action)), -1]) #0 previously
          break
        else:
          if new_distance < prev_distance and prev_score>=new_score:
            training_data.append([self.add_action_to_observation(obs, float(new_action)), 1])
          else:
            training_data.append([self.add_action_to_observation(obs, float(new_action)), 0]) #1 previosuly
          prev_distance=new_distance
          obs=self.generate_observation()
          prev_score=new_score
        #time.sleep (100.0 / 1000.0);
    return training_data
    
  def makeMoveAndCheckCollision(self,direction):
    for _ in [0,1]:self.theApp.player.update()#for update, as update count neens to be >2
    self.theApp.player.genericMove(direction)
    self.theApp.on_render()
    self.theApp.game.inLimit(self.theApp.windowWidth,self.theApp.windowHeight,self.theApp.player.x[0],self.theApp.player.y[0],44,self.theApp)
    self.theApp.checkAppleEaten()
    for i in range(2,self.theApp.player.length):
      self.theApp.game.isCollision(self.theApp.player.x[0],self.theApp.player.y[0],self.theApp.player.x[i], self.theApp.player.y[i],40,self.theApp)
      
  def getAppleDistance(self):
    return np.linalg.norm(np.array([self.theApp.apple.y-self.theApp.player.y[0],self.theApp.apple.x-self.theApp.player.x[0]]))
                          
  def normalize(self,vector):
    l=la.norm(vector)
    if l==0.0:
      return vector
    return vector/l
  
  def getAngle(self):
    snake_vector=[self.theApp.player.x[0],self.theApp.player.y[0]]
    #print(snake_vector)
    apple_vector=[self.theApp.apple.x-snake_vector[0],self.theApp.apple.y-snake_vector[1]]
    #direction=self.theApp.player.direction
    snake_vector=[snake_vector[0]-self.theApp.player.x[1],snake_vector[1]-self.theApp.player.y[1]]
    #print(snake_vector,apple_vector)
    snake_vector= self.normalize(np.array(snake_vector))#unit vector
    #print(snake_vector)
    apple_vector= self.normalize(np.array(apple_vector))#unit vector
    #print(apple_vector)
    
    cosang = np.dot(snake_vector,apple_vector)
    sinang = np.cross(snake_vector,apple_vector)
    return math.atan2(sinang, cosang)*180/np.pi
    #return np.arctan2(np.array([apple_vector[1],snake_vector[1]]))*180/np.pi
    #return np.arctan2(np.array([self.theApp.apple.x-self.theApp.player.x[0]]),np.array([self.theApp.apple.y-self.theApp.player.y[0]]))*180/np.pi
    
  def add_action_to_observation(self,obs,action):
    a=obs[:]
    a.append(action)
    return a
    
  def getSnakeDirection(self):
    return self.theApp.player.direction
    
  def action(self):#left or right random
    action=randint(-1,1)
    return action,self.getGameResultBasedOnAction(action)
    
  def generate_observation(self):
    #print("in generate_observation")
    l=self.isDirectionBlocked(-1)
    s=self.isDirectionBlocked(0)
    r=self.isDirectionBlocked(1)
    angle=self.getAngle()
    return [float(l),float(s),float(r),float(angle)/180]
    
  def isDirectionBlocked(self,action):
    x=self.theApp.player.x[0]
    y=self.theApp.player.y[0]
    l=self.getGameResultBasedOnAction(action)
    #print("action is "+str(l))
    x1=x
    y1=y
    if l==0:x1=self.theApp.player.right()
    elif l==1:x1=self.theApp.player.left()
    elif l==2:y1=self.theApp.player.up()
    elif l==3:y1=self.theApp.player.down()
    #print("x,y,x1,y1 "+str(x)+","+str(y)+","+str(x1)+","+str(y1))
    flag=False
    if self.theApp.game.inLimit(self.theApp.windowWidth,self.theApp.windowHeight,x1,y1,44):
      #check for self collision also
      flag=True
    #print(flag)
    for i in range(2,self.theApp.player.length-1):
      if self.theApp.game.isCollision(x1,y1,self.theApp.player.x[i], self.theApp.player.y[i],44):
        flag=True
        break
    #print(flag)
    return flag
    
  def getGameResultBasedOnAction(self,action):
    direction=self.getSnakeDirection()
    #print(direction)
    if action==0:
      return direction[1]
    new_direction=direction[:]
    new_direction[0]=new_direction[1]
    new_direction[1]=action
    #print(direction,new_direction)
    game_result=-1
    for pair in self.directions:
      if new_direction==pair[0]:
        #print("direction match")
        game_result=pair[1]
        break
    return game_result
    
  def NNmodel(self):
    model=Sequential()
    model.add(Dense(units=25,kernel_initializer="uniform",activation="relu",input_dim=5))
    model.add(Dense(units=1,kernel_initializer="uniform",activation="sigmoid"))
    #model.add(Dense(units=1,kernel_initializer="uniform",activation="sigmoid"))
    model.compile(optimizer="adam",loss="mean_squared_error",metrics=['accuracy'])
    return model
  
  def training(self):
    training_data=self.automatedMovesForSnake()
    a=np.array(training_data)
    X=a[:,0]
    X=np.array([np.array(xi) for xi in X])
    y=a[:,1]
    np.save("snake_train_test",a)
    self.model=self.NNmodel()
    print(X.shape)
    self.model.fit(X, y, epochs=3,shuffle=True)
    self.model.save("model_nn2_test.h5")
    print("game starting")
    #scores = self.model.evaluate(X, y)
    #print("\n%s: %.2f%%" % (self.model.metrics_names[1], scores[1]*100))
    for i in range(10000000):#delay to start game
      pass
    

  def test(self):
    model=keras.models.load_model("model_nn2_test.h5")
    for _ in range(self.testGames):
      self.theApp.reset()
      obs=self.generate_observation()
      for _ in range(self.goalSteps):
        predictions=[]
        for action in [-1,0,1]:
          a=np.array(self.add_action_to_observation(obs, float(action)) )
          a=a.reshape(1,5)
          predictions.append(model.predict(a))
        print(predictions)
        action=np.argmax(np.array(predictions))-1
        direction=self.getGameResultBasedOnAction(action)
        self.makeMoveAndCheckCollision(direction)
        if not self.theApp._running:
          break
        else:
          obs=self.generate_observation()
        time.sleep (200.0 / 1000.0);

if __name__=="__main__":
  snake=snake()
  snake.training()
  snake.test()
  
  
