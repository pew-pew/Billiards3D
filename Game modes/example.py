from gameController import *
import phisi as physics
import math

name = "Example"

description = """\
line1
Example game mode
line3
line4
line5
line5
"""

class GameController(BaseGameController):
    name = name
    description = description
    
    def gameInit(self):
        sizeX, sizeY, sizeZ = 500, 500, 500
        r = 40
        sp = r / 2
        
        self.box.sizeX = sizeX
        self.box.sizeY = sizeY
        self.box.sizeZ = sizeZ
        
        self.box.balls = [physics.Ball(230, 100, 310, 30, 1, 0, 0, 0),
                          physics.Ball(100, 100, 100, 30, 1, 0, 0, 0),
                          physics.Ball(100, 300, 400, 30, 1, 0, 0, 0)]
        
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
        
        self.mainBall = self.box.balls[0]
        self.mainBall.fillColor = (255, 255, 255)
        self.mainBall.canBeSelected = True
        self.box.balls[1].fillColor = (200, 30, 30)
        
        self.turnQ = 0
    
    def gameStart(self):
        self.setMessage("Turn " + str(self.turnQ))
    
    def gameTurn(self):
        self.turnQ += 1
        self.setMessage("Turn " + str(self.turnQ))
        
        print("Turn!")
        for ev in self.events:
            print(ev)
        
        for ev in self.events:
            if type(ev) is InHoleEvent:
                ball = ev.ball
                ball.placeAt(self.box.sizeX / 2, self.box.sizeY / 2, self.box.sizeZ / 2)
                print("Placed!")
        
        print()
