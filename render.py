import math
import phisi as physics
from PyQt5.Qt import *

def translate(x, y, z, dx, dy, dz):
    return (x + dx, y + dy, z + dz)

def rotateOX(x, y, z, rotOX):
    cos_ = math.cos(rotOX)
    sin_ = math.sin(rotOX)
    yn = y *  cos_ + z * sin_
    zn = y * -sin_ + z * cos_
    return (x, yn, zn)

def rotateOY(x, y, z, rotOY):
    cos_ = math.cos(rotOY)
    sin_ = math.sin(rotOY)
    xn = x * cos_ + z * -sin_
    zn = x * sin_ + z * cos_
    return (xn, y, zn)

def rotateOZ(x, y, z, rotOZ):
    cos_ = math.cos(rotOZ)
    sin_ = math.sin(rotOZ)
    xn = x * cos_ + y * -sin_
    yn = x * sin_ + y *  cos_
    return (xn, yn, z)

def rotate(x, y, z, rotOX, rotOY, rotOZ, reverse=False):
    if reverse:
        x, y, z = rotateOZ(x, y, z, rotOZ)
        x, y, z = rotateOX(x, y, z, rotOX)
        x, y, z = rotateOY(x, y, z, rotOY)
    else:
        x, y, z = rotateOY(x, y, z, rotOY)
        x, y, z = rotateOX(x, y, z, rotOX)
        x, y, z = rotateOZ(x, y, z, rotOZ)
    return (x, y, z)

class Camera:
    def __init__(self, box, viewWidth, viewHeight, x=0, y=0, z=0, rotOX=0, rotOY=0, rotOZ=0, perspective=False):
        self.box = box
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.x = x
        self.y = y
        self.z = z
        self.rotOX = rotOX
        self.rotOY = rotOY
        self.rotOZ = rotOZ
        self.perspective = perspective
        
        self.canvasWidth = None
        self.canvasHeight = None
        self.painter = None
        
        self.edges = []
        
        sizeX, sizeY, sizeZ = self.box.sizeX, self.box.sizeY, self.box.sizeZ
        
        for a in [0, 1]:
            for b in [0, 1]:
                self.edges.append([a, b, 0, a, b, 1])
                self.edges.append([a, 0, b, a, 1, b])
                self.edges.append([0, a, b, 1, a, b])
        
        for i in range(len(self.edges)):
            x1, y1, z1, x2, y2, z2 = self.edges[i]
            x1, x2 = x1 * sizeX, x2 * sizeX
            y1, y2 = y1 * sizeY, y2 * sizeY
            z1, z2 = z1 * sizeZ, z2 * sizeZ
            self.edges[i] = [x1, y1, z1, x2, y2, z2]
    
    def moveLocal(self, x, y, z):
        x, y, z = rotate(x, y, z, self.rotOX, self.rotOY, self.rotOZ, reverse=True)
        self.x += x
        self.y += y
        self.z += z
    
    def alignForCamera(self, x, y, z):
        x, y, z = translate(x, y, z, -self.x, -self.y, -self.z)
        x, y, z = rotate(x, y, z, -self.rotOX, -self.rotOY, -self.rotOZ)
        return (x, y, z)
    
    def transformPerspective(self, x, y, z):
        k = 300 / max(0.001, z)
        x *= k
        y *= k
        return (x, y, z)
    
    def alignForCanvas(self, x, y):
        kx = self.canvasWidth / self.viewWidth
        ky = self.canvasHeight / self.viewHeight
        x = (x + self.viewWidth / 2) * kx
        y = (y + self.viewHeight / 2) * ky
        y = self.canvasHeight - 1 - y
        return (x, y)
    
    def renderBackgound(self):
        self.painter.fillRect(0, 0, self.canvasWidth, self.canvasHeight, QBrush(Qt.white, Qt.SolidPattern))
    
    def render(self, painter, width, height):
        self.canvasWidth = width
        self.canvasHeight = height
        self.painter = painter
        
        #self.renderBackgound()
        
        #----align edges to camera----
        minZ = float("inf")
        alignedEdges = []
        for x1, y1, z1, x2, y2, z2 in self.edges:
            x1, y1, z1 = self.alignForCamera(x1, y1, z1)
            x2, y2, z2 = self.alignForCamera(x2, y2, z2)
            minZ = min(minZ, z1, z2)
            alignedEdges.append([x1, y1, z1, x2, y2, z2])
        
        #----align spheres to camera----
        alignedSpheres = []
        for ball in self.box.balls:
            if ball.isInHole():
                continue
            
            sphere = ball.sphere
            x, y, z, r = sphere.x, sphere.y, sphere.z, sphere.R
            x, y, z = self.alignForCamera(x, y, z)
            
            try:
                color = ball.color
            except:
                k = max(0, min(1, z / 300)) #  --------------------------------
                color = QColor(k * 255, 50, (1 - k) * 255)
            
            alignedSpheres.append([x, y, z, r, color])
        
        for hole in self.box.holes:
            sphere = hole.sphere
            x, y, z, r = sphere.x, sphere.y, sphere.z, sphere.R
            x, y, z = self.alignForCamera(x, y, z)
            alignedSpheres.append([x, y, z, r, QColor(0, 0, 0)])
        
        alignedSpheres.sort(reverse=True, key=lambda x: x[2])
        
        if self.perspective:
            #----render edges----
            painter.setPen(Qt.SolidLine)
            for x1, y1, z1, x2, y2, z2 in alignedEdges:
                x1, y1, z1 = self.transformPerspective(x1, y1, z1)
                x2, y2, z2 = self.transformPerspective(x2, y2, z2)
                x1, y1 = self.alignForCanvas(x1, y1)
                x2, y2 = self.alignForCanvas(x2, y2)
                self.painter.drawLine(x1, y1, x2, y2)
            
            #----render spheres----
            painter.setPen(Qt.SolidLine)
            for x, y, z, r, color in alignedSpheres:
                if z <= 0:
                    continue
                x1, y1 = x - r, y - r
                x2, y2 = x + r, y + r
                x1, y1, z1 = self.transformPerspective(x1, y1, z)
                x2, y2, z2 = self.transformPerspective(x2, y2, z)
                x1, y1 = self.alignForCanvas(x1, y1)
                x2, y2 = self.alignForCanvas(x2, y2)
                painter.setBrush(color)
                self.painter.drawEllipse(x1, y1, x2 - x1, y2 - y1)
        else:
            #----render far edges----
            painter.setPen(Qt.SolidLine)
            for x1, y1, z1, x2, y2, z2 in alignedEdges:
                if z1 == minZ or z2 == minZ:
                    continue
                x1, y1 = self.alignForCanvas(x1, y1)
                x2, y2 = self.alignForCanvas(x2, y2)
                self.painter.drawLine(x1, y1, x2, y2)
            
            #----render spheres----
            painter.setPen(Qt.SolidLine)
            for x, y, z, r, color in alignedSpheres:
                x1, y1 = x - r, y - r
                x2, y2 = x + r, y + r
                x1, y1 = self.alignForCanvas(x1, y1)
                x2, y2 = self.alignForCanvas(x2, y2)
                painter.setBrush(color)
                self.painter.drawEllipse(x1, y1, x2 - x1, y2 - y1)
            
            #----render 3 closest edges----
            #self.painter.setPen(Qt.DashLine)
            #for x1, y1, z1, x2, y2, z2 in alignedEdges:
                #if z1 != minZ and z2 != minZ:
                    #continue
                #x1, y1 = self.alignForCanvas(x1, y1)
                #x2, y2 = self.alignForCanvas(x2, y2)
                #self.painter.drawLine(x1, y1, x2, y2)
        
        self.canvasWidth = None
        self.canvasHeight = None
        self.painter = None
    
    def getBallAt(self, tx, ty):
        selected = None
        minZ = float("inf")
        if self.perspective:
            for ball in self.box.balls:
                sphere = ball.sphere
                x, y, z, r = sphere.x, sphere.y, sphere.z, sphere.R
                
                x, y, z = self.alignForCamera(x, y, z)
                x1, y1 = x - r, y - r
                x2, y2 = x + r, y + r
                x1, y1, z1 = self.transformPerspective(x1, y1, z)
                x2, y2, z2 = self.transformPerspective(x2, y2, z)
                
                x, y, z = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
                r = abs(x1 - x2) / 2
                
                if z <= 0 or ball.isInHole():
                    continue
                
                if (x - tx) ** 2 + (y- ty) ** 2 <= r ** 2:
                    if minZ > z:
                        selected = ball
                        minZ = z
        else:
            for ball in self.box.balls:
                if ball.isInHole():
                    continue
                sphere = ball.sphere
                x, y, z, r = sphere.x, sphere.y, sphere.z, sphere.R
                x, y, z = self.alignForCamera(x, y, z)
                if self.perspective:
                    pass
                if (x - tx) ** 2 + (y - ty) ** 2 <= r ** 2:
                    if minZ > z:
                        selected = ball
                        minZ = z
        return selected


class Communication(QObject):
    ballSelected = pyqtSignal(physics.Ball, Camera)


class CameraViewWidget(QWidget):
    def __init__(self, parent=None, camera=None):
        super().__init__(parent)
        self.camera = camera
        self.communication = Communication()
        self.ballSelected = self.communication.ballSelected
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        w = self.width()
        h = self.height()
        sizeMin = min(w, h)
        sizeMax = max(w, h)
        
        painter.fillRect(0, 0, w, h, QBrush(Qt.white, Qt.SolidPattern))
        painter.translate((w - sizeMin) / 2, (h - sizeMin) / 2)
        self.camera.render(painter, sizeMin, sizeMin)
    
    def onCamera(self, x, y):
        w = self.width()
        h = self.height()
        sizeMin = min(w, h)
        sizeMax = max(w, h)
        
        cw = self.camera.viewWidth
        ch = self.camera.viewHeight
        
        x = x - (w - sizeMin) / 2
        y = y - (h - sizeMin) / 2
        
        kx = sizeMin / cw
        ky = sizeMin / ch
        
        y = sizeMin - 1 - y
        y = y / ky - ch / 2
        x = x / kx - cw / 2
        
        return (x, y)
    
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            super().mousePressEvent(event)
            return
        
        x, y = event.x(), event.y()
        x, y = self.onCamera(x, y)
        
        ball = self.camera.getBallAt(x, y)
        
        if ball:
            self.communication.ballSelected.emit(ball, self.camera)
            return
        
        super().mousePressEvent(event)