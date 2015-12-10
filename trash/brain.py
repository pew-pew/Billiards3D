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
        x, y, z = rotate(x, y, z, self.rotOX, self.rotOY, self.rotOZ)
        self.x += x
        self.y += y
        self.z += z
    
    def trans(self, x, y, z):
        x, y, z = translate(x, y, z, -self.x, -self.y, -self.z)
        x, y, z = rotate(x, y, z, -self.rotOX, -self.rotOY, -self.rotOZ)
        return (x, y, z)
    
    def transCanv(self, x, y, kx, ky):
        x = x + self.width / 2
        y = y + self.height / 2
        return (x * kx, y * ky)
    
    def render(self, painter, width, height):
        kx = width / self.width
        ky = height / self.height        

        painter.fillRect(0, 0, width, height, QBrush(Qt.white, Qt.SolidPattern))
        
        sz = 300
        edges = [[0, 0, 0, 0, 0, sz],
                 [0, 0, 0, 0, sz, 0],
                 [0, 0, 0, sz, 0, 0],
                 [sz, sz, sz, 0, sz, sz],
                 [sz, sz, sz, sz, sz, 0],
                 [sz, sz, sz, sz, 0, sz],
                 
                 #[0, 0, sz, sz, 0, sz],
                 #[0, sz, 0, sz, sz, 0],
                 
                 #[sz, 0, sz, 0, sz, 0],
                 #[0, 0, sz, sz, sz, 0],

                 #[sz, 0, 0, 0, sz, sz],
                 #[0, sz, 0, sz, 0, sz],
                 ]
        
        for edge in edges:
            x1, y1, z1, x2, y2, z2 = edge
            x1, y1, z1 = self.trans(x1, y1, z1)
            x2, y2, z2 = self.trans(x2, y2, z2)
            x1, y1 = self.transCanv(x1, y1, kx, ky)
            x2, y2 = self.transCanv(x2, y2, kx, ky)
            painter.drawLine(x1, y1, x2, y2)
        
        
        spheres = []
        for ball in self.box.balls:
            x, y, z, r = ball.sphere.x, ball.sphere.y, ball.sphere.z, ball.sphere.R
            x, y, z = translate(x, y, z, -self.x, -self.y, -self.z)
            x, y, z = rotate(x, y, z, -self.rotOX, -self.rotOY, -self.rotOZ)
            spheres.append([z, x, y, r])
        
        spheres.sort(reverse=True)
        
        for sphere in spheres:
            z, x, y, r = sphere
            #if z < 0: continue
            
            rectX = (x - r + self.width / 2) * kx
            rectY = (y - r + self.height / 2) * ky
            rectW = r * 2 * kx
            rectH = r * 2 * ky
            
            k = min(1, max(0, abs(z) / 300))
            
            painter.setBrush(QColor(0, 255 * k, (1 - k) * 255))
            painter.drawEllipse(rectX, rectY, rectW, rectH)


class CameraViewWidget(QWidget):
    def __init__(self, parent=None, camera=None):
        super().__init__(parent)
        self.camera = camera
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setTransform(painter.transform().translate(0, self.height() - 1).scale(1, -1))
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
                                                               x=150, y=150, z=0))
        
        vbox = QHBoxLayout()
        vbox.addWidget(self.cameraView)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(vbox)
    
    def initBox(self):
        sizeX, sizeY, sizeZ = 300, 300, 300
        
        #             physics.Ball(x, y, z, R, m, vx, vy, vz)
        self.balls = [#physics.Ball(250, 130, 150, 20, 1, 1.5, 0.3, 0),
                      #physics.Ball(200, 160, 150, 20, 1, 1, 2, 0),
                      #physics.Ball(50, 60, 150, 20, 1, 2, 0.5, 0),
                      physics.Ball(100, 200, 200, 20, 0, 0, 0, 0),
                      physics.Ball(100, 200, 100, 20, 0, 0, 0, 0),
                      physics.Ball(100, 100, 200, 20, 0, 0, 0, 0),
                      physics.Ball(100, 100, 100, 20, 0, 0, 0, 0),
                      physics.Ball(200, 200, 200, 20, 0, 0, 0, 0),
                      physics.Ball(200, 200, 100, 20, 0, 0, 0, 0),
                      physics.Ball(200, 100, 200, 20, 0, 0, 0, 0),
                      physics.Ball(200, 100, 100, 20, 0, 0, 0, 0),
                      ]
        self.holes = []
        self.box = physics.Box(300, 300, 300, self.balls, self.holes, 0, 0)
    
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