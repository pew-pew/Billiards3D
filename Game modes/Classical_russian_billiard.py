from gameController import *
import phisi as physics
import math

name = "Classical_russian_billiard"

description = """\
The original game
"""

class GameController(BaseGameController):
    def gameInit(self):
        sizeX, sizeY, sizeZ = 1750, 875, 875
        r = 40
        sp = r / 2
        
        self.box.sizeX = sizeX
        self.box.sizeY = sizeY
        self.box.sizeZ = sizeZ
        
        self.box.balls = [physics.Ball(437, 437, 437, 20, 1, 0, 0, 0),
                      physics.Ball(1000 - 1, 437, 437, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 + 22, 437 + 22, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 - 22, 437 + 22, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 + 22, 437 - 22, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 - 22, 437 - 22, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437, 437, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 + 44, 437 + 44, 20, 1, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 - 44, 437 + 44, 20, 1, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 + 44, 437 - 44, 20, 1, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 - 44, 437 - 44, 20, 1, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437, 437 + 44, 20, 1, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 + 44, 437, 20, 1, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437, 437 - 44, 20, 1, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 - 44, 437, 20, 1, 0, 0, 0)
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
        
        self.taggedColor = (250, 250, 250)
        self.untaggedColor = (160, 160, 160)
        self.mistakes = 0
    
    def gameStart(self):
        for ball in self.box.balls:
            ball.fillColor = self.untaggedColor
        self.taggedBall.fillColor = self.taggedColor
        self.taggedBall.canBeSelected = True
        self.wasHit = False
    
    def ballHitEvent(self, ball1, ball2):
        balls = (ball1, ball2)
        
        self.wasHit = True
                
    def gameTurn(self):
        if not self.wasHit:
            self.mistakes += 1
        
        if self.mistakes >= 1:
            self.setMessage("You lose!")
        
        for ball in self.box.balls:
            ball.canBeSelected = True
            if ball is not self.taggedBall:
                if not ball.isInHole():
                    break
        else:
            self.setMessage("You win!")