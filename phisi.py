from plani import * #/KDqDmyKg
import sys

class Hole:
    def __init__(self, x, y, z, R):
        self.sphere = Sphere(x, y, z, R)
        
    def score(self, ball):
        if dist(self.sphere, ball.misticsphere) < 0:
            ball.speed = Vector(0, 1000000, 0)
            points -= 1
            
    
class Ball:
    def __init__(self, x, y, z, R, m, vx, vy, vz):
        self.sphere = Sphere(x, y, z, R)
        self.m = m
        self.speed = Vector(vx, vy, vz)
        self.Nspeed = Vector(vx, vy, vz)
        self.misticsphere = Sphere(x + vx, y + vy, z + vz, R)
        
        self._inHole = False
        
    def move(self):
        self.speed = self.Nspeed
        self.sphere.x += self.speed.x
        self.sphere.y += self.speed.y
        self.sphere.z += self.speed.z
        self.misticsphere.x += self.speed.x
        self.misticsphere.y += self.speed.y
        self.misticsphere.z += self.speed.z
        
    def dist(self, other):
        return self.sphere.dist(other.sphere)
    
    
    def isInHole(self):
        return self._inHole    
    
    def _isInHole(self, hole):
        return (Sphere(hole.sphere.x, hole.sphere.y, hole.sphere.z, hole.sphere.R - self.misticsphere.R).dist(self.misticsphere)) < 0
    
    def resistanse(self, resistanse):
        #           V      speed changed to Nspeed!------------------------------------------
        if abs(self.Nspeed) < 0.1:
            self.Nspeed = Vector(0, 0, 0)
        else:
            self.speed.x = self.speed.x - self.speed.x * resistanse
            self.speed.y = self.speed.y - self.speed.y * resistanse
            self.speed.z = self.speed.z - self.speed.z * resistanse
        
    def hit(self, direction, forse):
        self.Nspeed += direction * forse * (1 / self.m)
    
    def wall(self, SIZE_X, SIZE_Y, SIZE_Z, wall_resistanse):
        if self.misticsphere.x - self.sphere.R <= 0 or self.misticsphere.x + self.sphere.R >= SIZE_X:
            self.speed.x = self.speed.x * (-1 + wall_resistanse)
            return True
        if self.misticsphere.y - self.sphere.R <= 0 or self.misticsphere.y + self.sphere.R >= SIZE_Y:
            self.speed.y = self.speed.y * (-1 + wall_resistanse)
            return True
        if self.misticsphere.z - self.sphere.R <= 0 or self.misticsphere.z + self.sphere.R >= SIZE_Z:
            self.speed.z = self.speed.z * (-1 + wall_resistanse)
            return True
        return False
        
    def crash(self, other):
        self.Nspeed, other.Nspeed = bump(self.Nspeed, other.Nspeed, Vector(self.sphere.x - other.sphere.x, self.sphere.y - other.sphere.y, self.sphere.z - other.sphere.z))
    
    def placeAt(self, x, y, z):
        self.speed = Vector(0, 0, 0)
        self.Nspeed = Vector(0, 0, 0)
        self.sphere = Sphere(x, y, z, self.sphere.R)
        self.misticsphere = Sphere(x, y, z, self.sphere.R)
        
        self._inHole = False
        
        

class Box:
    def __init__(self,  sizeX, sizeY, sizeZ, balls, holes, resistanse, wall_resistanse):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.balls = balls
        self.holes = holes
        self.resistanse = resistanse
        self.wall_resistanse = wall_resistanse
        
        self.ballHitCallback = None
        self.wallHitCallback = None
        self.inHoleCallback = None

    def movement(self):
        ballsForCheck = list(filter(lambda b: not b.isInHole(), self.balls))
        
        for ball in ballsForCheck:
            result = ball.wall(self.sizeX, self.sizeY, self.sizeZ, self.wall_resistanse)
            if result and self.wallHitCallback:
                self.wallHitCallback(ball)
        
        for ball in ballsForCheck:
            ball.resistanse(self.resistanse)
        
        for i in range(len(ballsForCheck)):
            for j in range(i + 1, len(ballsForCheck)):
                if ballsForCheck[i].dist(ballsForCheck[j]) <= 0:
                    ballsForCheck[i].crash(ballsForCheck[j])
                    self.ballHitCallback(ballsForCheck[i], ballsForCheck[j])
        
        for ball in ballsForCheck:
            ball.move()
        
        for ball in ballsForCheck:
            for hole in self.holes:
                if ball._isInHole(hole):
                    ball._inHole = True
                    if self.inHoleCallback:
                        self.inHoleCallback(ball, hole)
        