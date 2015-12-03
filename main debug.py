import sys
from PyQt5.Qt import *
import phisi as physics
import plani as planimetry
from collections import deque

class Camera:
    def __init__(self, box, smt=lambda *args: args):
        self.box = box
        self.smt = smt
    
    def render(self, painter):
        painter.fillRect(0, -0, 300, 300, QBrush(Qt.white, Qt.SolidPattern))
        for ball in self.box.balls:
            x, y, z, r = ball.sphere.x, ball.sphere.y, ball.sphere.z, ball.sphere.R
            x, y, z = self.smt(x, y, z)
            depth = z / 300
            
            painter.setBrush(QColor(depth * 255, (1 - depth) * 255, 0))
            painter.drawEllipse(x - r, y - r, r * 2, r * 2)

class CameraViewWidget(QWidget):
    def __init__(self, parent=None, camera=None):
        super().__init__(parent)
        self.camera = camera
        self.setFixedSize(300, 300)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setTransform(painter.transform().scale(0.5, 0.2))
        self.camera.render(painter)

class SIW(QWidget):
    def __init__(self, parent=None, box=None):
        super().__init__(parent)
        
        self.box = box
        self.cameraXY = Camera(box)
        self.cameraXZ = Camera(box, lambda x, y, z: (x, z, y))
        self.cameraYZ = Camera(box, lambda x, y, z: (y, z, x))
        
        self.setFixedSize(600, 600)
    
    def paintEvent(self, event):
        painterXY = QPainter(self)
        #painterXZ = QPainter(self)
        #painterYZ = QPainter(self)
        
        painterXY.translate(300, 300)
        #painterXZ.translate(300, 300)
        #painterYZ.translate(300, 300)
        
        painterXY.rotate(-30)
        

        
        self.cameraXY.render(painterXY)

class BilliardsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.initBox()
        self.initBaseProperties()
        
        self.timer = QBasicTimer()
        self.timer.start(10, self)
        
        #self.cameraView1 = CameraViewWidget(camera=Camera(self.box))
        #self.cameraView2 = CameraViewWidget(camera=Camera(self.box, lambda x, y, z: (x, z, y)))
        #self.cameraView3 = CameraViewWidget(camera=Camera(self.box, lambda x, y, z: (y, z, x)))
        self.siw = SIW(self, self.box)
        
        vbox = QHBoxLayout()
        #vbox.addWidget(self.cameraView1)
        #vbox.addWidget(self.cameraView2)
        #vbox.addWidget(self.cameraView3)
        vbox.addWidget(self.siw)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(vbox)
    
    def initBaseProperties(self):
        #self.setFixedSize(300, 300)
        self.move(300, 300)
    
    def initBox(self):
        sizeX, sizeY, sizeZ = 300, 300, 300
        
        #             physics.Ball(x, y, z, R, m, vx, vy, vz)
        self.balls = [physics.Ball(250, 130, 150, 20, 1, 1.5, 0.3, 0),
                      physics.Ball(200, 160, 150, 20, 1, 1, 2, 0),
                      physics.Ball(50, 60, 150, 20, 1, 2, 0.5, 1),
                      ]
        self.holes = []
        self.box = physics.Box(300, 300, 300, self.balls, self.holes, 0, 0)
    
    def paintEvent(self, event):
        physics.Box.movement(self.box)
    
    def timerEvent(self, event):
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BilliardsWidget()
    widget.show()
    sys.exit(app.exec_())