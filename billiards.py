import sys
from PyQt5.Qt import*
import phisi as physics
import plani as planimetry
from render import *


class BilliardsWidget(QWidget):
    def __init__(self, parent=None, box=physics.Box(300, 300, 300, [], [], 0.01, 0)):
        super().__init__(parent)
        
        self.box = box
        if not parent:
            self.initWindowGeometry()
        self.initWidgets()
        
        self.spectatorSpeed = [0, 0, 0]
        self.lastMousePos = None
        
        self.timer = QBasicTimer()
        self.timer.start(10, self)
        
        self.cameraView.ballSelected.connect(self.ballSelected)
    
    def initWindowGeometry(self):
        #self.resize(1000, 500)
        #self.move(300, 150)
        pass
        
    def initCamera(self):
        sizeX = self.box.sizeX
        sizeY = self.box.sizeY
        sizeZ = self.box.sizeZ
        
        camera = Camera(self.box,
                        viewWidth=sizeX*1.5, viewHeight=sizeY*1.5,
                        x=(sizeX / 2), y=(sizeY / 2), z=(sizeZ / 2))
        
        cameraView = CameraViewWidget(None, camera)
        
        cameraP = Camera(self.box,
                        viewWidth=sizeX*1.5, viewHeight=sizeY*1.5,
                        x=(sizeX / 2), y=(sizeY / 2), z=(sizeZ / 2),
                        perspective=True)
        cameraViewP = CameraViewWidget(None, cameraP)
        
        
        self.camera = camera
        self.cameraView = cameraView
        self.cameraP = cameraP
        self.cameraViewP = cameraViewP
    
    def initWidgets(self):
        self.initCamera()
        
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.cameraView)
        hbox.addWidget(self.cameraViewP)
        
        self.setLayout(hbox)
    
    #def resizeEvent(self, event):
        #self.cameraView.resize(self.size())
    
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
        self.camera.rotOX -= dy / 100
        self.camera.rotOY -= dx / 100
        self.cameraP.rotOX -= dy / 100
        self.cameraP.rotOY -= dx / 100
        
        self.lastMousePos = [x, y]
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastMousePos = None
    
    def ballSelected(self, ball, camera):
        if camera.perspective:
            pass #  shuold be something-------------------------
        else:
            x, y, z = rotate(0, 0, 1, camera.rotOX, camera.rotOY, camera.rotOZ, reverse=True)
            f = 5
            
            direction = planimetry.Vector(x, y, z)
            ball.hit(direction, f)

    def timerEvent(self, event):
        self.camera.moveLocal(*self.spectatorSpeed)
        self.cameraP.moveLocal(*self.spectatorSpeed)
        
        self.box.movement()
        self.update()

if __name__ == "__main__":
    sizeX, sizeY, sizeZ = 500, 500, 500
    r = 40
    sp = r / 2
    
    balls = [physics.Ball(100, 100, 400, 20, 1, 0, 0, 0),
             physics.Ball(100, 100, 100, 20, 1, 0, 0, 0),
             physics.Ball(100, 300, 400, 20, 1, 0, 0, 0)]
    
    
    
    holes = [physics.Hole(sp, sp, sp, r), 
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
    
    box = physics.Box(sizeX, sizeY, sizeZ, balls, holes, 0.005, 0.005)
    
    
    
    app = QApplication(sys.argv)
    widget = BilliardsWidget(box=box)
    widget.resize(1000, 500)
    widget.show()
    
    sys.exit(app.exec_())