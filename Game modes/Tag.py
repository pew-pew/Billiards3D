from gameController import *
import phisi as physics
import math

name = "Tag"

description = """\
Ваша цель - забить все шары, но бить вы можете только по красному.
Главная сложность в том, что красный цвет передаётся другому шару при столкновении.
Поэтому если вы забьёте красный шар, оставив на поле несколько серых, то вы проиграли!
"""

class GameController(BaseGameController):
    def gameInit(self):
        sizeX, sizeY, sizeZ = 500, 500, 500
        r = 40
        sp = r / 2
        
        self.box.sizeX = sizeX
        self.box.sizeY = sizeY
        self.box.sizeZ = sizeZ
        
        self.box.balls = [physics.Ball(230, 100, 310, 30, 1, 0, 0, 0),
                          physics.Ball(100, 100, 100, 30, 1, 0, 0, 0),
                          physics.Ball(200, 300, 400, 30, 1, 0, 0, 0),
                          #physics.Ball(200, 250, 200, 30, 1, 0, 0, 0),
                          #physics.Ball(200, 100, 200, 30, 1, 0, 0, 0),
                          #physics.Ball(100, 300, 300, 30, 1, 0, 0, 0),
                          ]
        
        self.box.holes = [physics.Hole(sp, sp, sp, r), 
                          physics.Hole(sizeX - sp, sp, sp, r), 
                          physics.Hole(sp, sizeY - sp, sp, r),
                          physics.Hole(sp, sp, sizeZ - sp, r), 
                          physics.Hole(sizeX - sp, sizeY - sp, sp, r),
                          physics.Hole(sizeX - sp, sp, sizeZ - sp, r),
                          physics.Hole(sp, sizeY - sp, sizeZ - sp, r),
                          physics.Hole(sizeX - sp, sizeY - sp, sizeZ - sp, r),
                          physics.Hole(sizeX // 2, sizeY - sp, sizeZ - sp, r),
                          physics.Hole(sizeX // 2, sizeY - sp, sp, r), 
                          physics.Hole(sizeX // 2, sp, sizeZ - sp, r),
                          physics.Hole(sizeX // 2, sp, sp, r),
                          ]
        
        self.taggedBall = self.box.balls[0]
        
        self.taggedColor = (220, 30, 30)
        self.untaggedColor = (160, 160, 160)
    
    def gameStart(self):
        for ball in self.box.balls:
            ball.fillColor = self.untaggedColor
        self.taggedBall.fillColor = self.taggedColor
        self.taggedBall.canBeSelected = True
    
    def ballHitEvent(self, ball1, ball2):
        balls = (ball1, ball2)
        
        if self.taggedBall not in balls:
            return
        
        if balls[0] is self.taggedBall:
            newTaggedBall = balls[1]
        else:
            newTaggedBall = balls[0]
            
        self.taggedBall.canBeSelected = False
        self.taggedBall.fillColor = self.untaggedColor
        
        newTaggedBall.canBeSelected = True
        newTaggedBall.fillColor = self.taggedColor
        
        self.taggedBall = newTaggedBall
    
    def gameTurn(self):
        if self.taggedBall.isInHole():
            self.setMessage("You lose!")
        
        for ball in self.box.balls:
            if not ball.isInHole():
                break
        else:
            self.setMessage("You win!")