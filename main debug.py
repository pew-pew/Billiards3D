import sys
from PyQt5.Qt import *
import phisi as physics
import plani as planimetry
import math

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

def rotate(x, y, z, rotOX, rotOY, rotOZ):
    x, y, z = rotateOY(x, y, z, rotOY)
    x, y, z = rotateOX(x, y, z, rotOX)
    x, y, z = rotateOZ(x, y, z, rotOZ)
    return (x, y, z)

class Camera:
    def __init__(self, box, width, height, x=0, y=0, z=0, rotOX=0, rotOY=0, rotOZ=0):
        self.box = box
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.z = z
        self.rotOX = rotOX
        self.rotOY = rotOY
        self.rotOZ = rotOZ
    
    def moveLocal(self, x, y, z):
        x, y, z = rotateOZ(x, y, z, self.rotOZ)
        x, y, z = rotateOX(x, y, z, self.rotOX)
        x, y, z = rotateOY(x, y, z, self.rotOY)
        self.x += x
        self.y += y
        self.z += z
    
    def trans(self, x, y, z):
        x, y, z = translate(x, y, z, -self.x, -self.y, -self.z)
        x, y, z = rotate(x, y, z, -self.rotOX, -self.rotOY, -self.rotOZ)
        return (x, y, z)
    
    def transCanv(self, x, y, z, width, height):
        k = 1000 / max(z, 0.1)
        x *= k
        y *= k
        kx = width / self.width
        ky = height / self.height
        x = (x + self.width / 2) * kx
        y = (y + self.height / 2) * ky
        y = height - 1 - y
        return (x, y)
    
    def render(self, painter, width, height):      
        painter.fillRect(0, 0, width, height, QBrush(Qt.white, Qt.SolidPattern))
        
        sizeX, sizeY, sizeZ = self.box.sizeX, self.box.sizeY, self.box.sizeZ
        edges = [[0, 0, 0, 0, 0, sizeZ],
                 [0, 0, 0, 0, sizeY, 0],
                 [0, 0, 0, sizeX, 0, 0],
                 [sizeX, sizeY, sizeZ, 0, sizeY, sizeZ],
                 [sizeX, sizeY, sizeZ, sizeX, sizeY, 0],
                 [sizeX, sizeY, sizeZ, sizeX, 0, sizeZ],
                 
                 [0, 0, sizeZ, sizeX, 0, sizeZ],
                 [0, sizeY, 0, sizeX, sizeY, 0],
                 
                 [sizeX, 0, 0, sizeX, sizeY, 0],
                 [0, 0, sizeZ, 0, sizeY, sizeZ],

                 [sizeX, 0, 0, sizeX, 0, sizeZ],
                 [0, sizeY, 0, 0, sizeY, sizeZ],
                 ]
        
        minZ = float("inf")
        for i in range(len(edges)):
            x1, y1, z1, x2, y2, z2 = edges[i]
            x1, y1, z1 = self.trans(x1, y1, z1)
            x2, y2, z2 = self.trans(x2, y2, z2)
            edges[i] = [x1, y1, z1, x2, y2, z2]
            minZ = min(minZ, z1, z2)
        
        painter.setPen(Qt.SolidLine)        
        for edge in edges:
            x1, y1, z1, x2, y2, z2 = edge
            if (z1 != minZ and z2 != minZ):
                x1, y1 = self.transCanv(x1, y1, z1, width, height)
                x2, y2 = self.transCanv(x2, y2, z2, width, height)
                painter.drawLine(x1, y1, x2, y2)
        
        spheres = []
        for ball in self.box.balls:
            if not ball.isInHole(self.box.holes):
                x, y, z, r = ball.sphere.x, ball.sphere.y, ball.sphere.z, ball.sphere.R
                x, y, z = translate(x, y, z, -self.x, -self.y, -self.z)
                x, y, z = rotate(x, y, z, -self.rotOX, -self.rotOY, -self.rotOZ)
                spheres.append([z, x, y, r, 'ball'])
            
        for hole in self.box.holes:
            x, y, z, r = hole.sphere.x, hole.sphere.y, hole.sphere.z, hole.sphere.R
            x, y, z = translate(x, y, z, -self.x, -self.y, -self.z)
            x, y, z = rotate(x, y, z, -self.rotOX, -self.rotOY, -self.rotOZ)
            spheres.append([z, x, y, r, 'hole'])            
        
        spheres.sort(reverse=True)
        painter.setPen(Qt.SolidLine)
        for sphere in spheres:
            z, x, y, r, ball_hole = sphere
            #if z < 0: continue
            
            x0, y0 = self.transCanv(x - r, y - r, z, width, height)
            x1, y1 = self.transCanv(x + r, y + r, z, width, height)
            
            k = min(1, max(0, z / (sizeX ** 2 + sizeY ** 2 + sizeZ ** 2) ** 0.5))
            
            if ball_hole == 'ball':
                painter.setBrush(QColor(0, 255 * (1 - k), 255 * k))
            else:
                painter.setBrush(QColor(0, 0, 0))
            painter.drawEllipse(x0, y0, x1 - x0, y1 - y0)
            #painter.drawText((x0 + x1) / 2 , (y0 + y1) / 2, str(int(z)))
        
        painter.setPen(Qt.DashLine)           
        for edge in edges:
            x1, y1, z1, x2, y2, z2 = edge
            if (z1 == minZ or z2 == minZ):
                x1, y1 = self.transCanv(x1, y1, z1, width, height)
                x2, y2 = self.transCanv(x2, y2, z2, width, height)
                painter.drawLine(x1, y1, x2, y2)


class CameraViewWidget(QWidget):
    def __init__(self, parent=None, camera=None):
        super().__init__(parent)
        self.camera = camera
    
    def paintEvent(self, event):
        painter = QPainter(self)
        #painter.setTransform(painter.transform().translate(0, self.height() - 1).scale(1, -1))
        self.camera.render(painter, self.width(), self.height())


class BilliardsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.initBox()
        self.initBaseProperties()
        self.initWidgets()
        
        self.spectatorSpeed = [0, 0, 0]
        self.lastMousePos = None
        
        self.trigger = 0
        
        self.timer = QBasicTimer()
        self.timer.start(10, self)
    
    def initBaseProperties(self):
        self.resize(600, 600)
        self.move(300, 150)
    
    def initWidgets(self):
        self.cameraView = CameraViewWidget(self, camera=Camera(self.box,
                                                               width=600, height=600,
                                                               x=100, y=437, z=437))
        
        vbox = QHBoxLayout()
        vbox.addWidget(self.cameraView)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(vbox)
    
    def initBox(self):
        sizeX, sizeY, sizeZ = 1750, 875, 875
        
        #             physics.Ball(x, y, z, R, m, vx, vy, vz)
        self.balls = [#physics.Ball(250, 130, 150, 20, 1, 1.5, 0.3, 1),
                      #physics.Ball(200, 160, 150, 20, 1, 1, 2, 1),
                      physics.Ball(150, 150, 150, 20, 1, -1, -1, -1),
                      physics.Ball(437, 437, 437, 20, 0, 10, 0, 0),
                      physics.Ball(1000 - 1, 437, 437, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 + 22, 437 + 22, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 - 22, 437 + 22, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 + 22, 437 - 22, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) + 2, 437 - 22, 437 - 22, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437, 437, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 + 44, 437 + 44, 20, 0, 0, 0, 0),
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 - 44, 437 + 44, 20, 0, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 + 44, 437 - 44, 20, 0, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 - 44, 437 - 44, 20, 0, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437, 437 + 44, 20, 0, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 + 44, 437, 20, 0, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437, 437 - 44, 20, 0, 0, 0, 0), 
                      physics.Ball(1000 + int(20 * 2 ** 0.5) * 2 + 4, 437 - 44, 437, 20, 0, 0, 0, 0)
                      ]

        self.holes = [physics.Hole(0, 0, 0, 45), 
                      physics.Hole(sizeX, 0, 0, 45), 
                      physics.Hole(0, sizeY, 0, 45),
                      physics.Hole(0, 0, sizeZ, 45), 
                      physics.Hole(sizeX, sizeY, 0, 45),
                      physics.Hole(sizeX, 0, sizeZ, 45),
                      physics.Hole(0, sizeY, sizeZ, 45),
                      physics.Hole(sizeX, sizeY, sizeZ, 45),
                      physics.Hole(sizeX // 2, sizeY, sizeZ, 45),
                      physics.Hole(sizeX // 2, sizeY, 0, 45), 
                      physics.Hole(sizeX // 2, 0, sizeZ, 45),
                      physics.Hole(sizeX // 2, 0, 0, 45)]
        self.box = physics.Box(sizeX, sizeY, sizeZ, self.balls, self.holes, 0.003, 0.003)
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_A:
            self.spectatorSpeed[0] -= 1
        if key == Qt.Key_D:
            self.spectatorSpeed[0] += 1
        if key == Qt.Key_Q:
            self.spectatorSpeed[1] -= 1
        if key == Qt.Key_E:
            self.spectatorSpeed[1] += 1
        if key == Qt.Key_S:
            self.spectatorSpeed[2] -= 1
        if key == Qt.Key_W:
            self.spectatorSpeed[2] += 1
    
    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_A:
            self.spectatorSpeed[0] += 1
        if key == Qt.Key_D:
            self.spectatorSpeed[0] -= 1
        if key == Qt.Key_Q:
            self.spectatorSpeed[1] += 1
        if key == Qt.Key_E:
            self.spectatorSpeed[1] -= 1
        if key == Qt.Key_S:
            self.spectatorSpeed[2] += 1
        if key == Qt.Key_W:
            self.spectatorSpeed[2] -= 1
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastMousePos = [event.x(), event.y()]
    
    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton or not self.lastMousePos:
            return
        
        x, y = event.x(), event.y()
        lastX, lastY = self.lastMousePos
        dx, dy = x - lastX, y - lastY
        self.cameraView.camera.rotOX -= dy / 100
        self.cameraView.camera.rotOY -= dx / 100
        
        self.lastMousePos = [x, y]
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastMousePos = None
        
        
    
    def timerEvent(self, event):
        self.cameraView.camera.moveLocal(*self.spectatorSpeed)
        #if self.trigger:
            #self.cameraView.camera.rotOY += 0.01
        #else:
            #self.cameraView.camera.rotOY -= 0.01
        
        self.trigger ^= 1
        
        self.box.movement()
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BilliardsWidget()
    widget.show()
    sys.exit(app.exec_())