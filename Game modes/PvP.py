from gameController import *
import phisi as physics
import math

name = "PvP"

description = """\
Two players
Eight balls 
"""

class GameController(BaseGameController):
    def gameInit(self):
        sizeX, sizeY, sizeZ = 500, 500, 500
        r = 40
        sp = r / 2
        
        self.box.sizeX = sizeX
        self.box.sizeY = sizeY
        self.box.sizeZ = sizeZ
       
        self.box.balls = [physics.Ball(125, 125, 125, 30, 1, 0, 0, 0),
                          physics.Ball(125, 375, 125, 30, 1, 0, 0, 0),
                          physics.Ball(125, 125, 375, 30, 1, 0, 0, 0),
                          physics.Ball(375, 125, 125, 30, 1, 0, 0, 0),
                          physics.Ball(375, 375, 125, 30, 1, 0, 0, 0),
                          physics.Ball(125, 375, 375, 30, 1, 0, 0, 0),
                          physics.Ball(375, 125, 375, 30, 1, 0, 0, 0),
                          physics.Ball(375, 375, 375, 30, 1, 0, 0, 0)
                          ]
        
        self.box.holes = [physics.Hole(sp, sp, sp, r), 
                          physics.Hole(sizeX - sp, sp, sp, r), 
                          physics.Hole(sp, sizeY - sp, sp, r),
                          physics.Hole(sp, sp, sizeZ - sp, r), 
                          physics.Hole(sizeX - sp, sizeY - sp, sp, r),
                          physics.Hole(sizeX - sp, sp, sizeZ - sp, r),
                          physics.Hole(sp, sizeY - sp, sizeZ - sp, r),
                          physics.Hole(sizeX - sp, sizeY - sp, sizeZ - sp, r),
                          physics.Hole(sizeX // 2, sizeY // 2, sizeZ // 2, r)                         
                          ]
        
        self.taggedBall = self.box.balls[3]
        
        self.taggedColor = (250, 250, 250)
        self.untaggedColor = (160, 160, 160)
        self.mistakes = 0
        self.score1 = 0
        self.score2 = 0
        self.tableballs = self.box.balls
    
    def gameStart(self):
        self.setMessage("First is playing")
        for ball in self.box.balls:
            ball.fillColor = self.untaggedColor
        self.taggedBall.fillColor = self.taggedColor
        self.taggedBall.canBeSelected = True
        self.wasHit = False
        self.player = 'first'
    
    def ballHitEvent(self, ball1, ball2):
        balls = (ball1, ball2)
        self.wasHit = True
                
    def gameTurn(self):
        oldtableballs = self.tableballs
        self.tableballs = []
        for ball in self.box.balls:
            if not ball.isInHole():
                self.tableballs.append(ball)
                
        if not self.wasHit:
            if self.player == 'first':
                self.score1 -= 1
            else:
                self.score2 -= 1        
        
        if len(oldtableballs) - len(self.tableballs) > 0:
            if self.player == 'first':
                self.score1 += len(oldtableballs) - len(self.tableballs)
            else:
                self.score2 += len(oldtableballs) - len(self.tableballs)
        else:
            if self.player == 'first':
                self.player = 'second'
                self.setMessage("Second is playing") 
            else:
                self.player = 'first'
                self.setMessage("First is playing")
                                
        if len(self.tableballs) < 2:
            self.setMessage("First " + str(score1) + ", " + "Second " + str(score2))
            
