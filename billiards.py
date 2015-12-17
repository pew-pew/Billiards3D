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
        
        self.spectatorSpeedDirection = [0, 0, 0]
        self.spectatorSpeedValue = 1
        
        self.selectedBall = None
        self.hitDirection = planimetry.Vector(0, 0, 0)
        self.hitForce = 5
        
        self.lastMousePos = None
        
        self.timer = QBasicTimer()
        self.timer.start(10, self)
    
    def initWindowGeometry(self):
        #self.resize(1000, 500)
        #self.move(300, 150)
        pass
        
    def initCamera(self):
        sizeX = self.box.sizeX
        sizeY = self.box.sizeY
        sizeZ = self.box.sizeZ
        
        #camera = Camera(self.box,
                        #viewWidth=sizeX*1.5, viewHeight=sizeY*1.5,
                        #x=(sizeX / 2), y=(sizeY / 2), z=(sizeZ / 2))
        
        #cameraView = CameraViewWidget(None, camera)
        
        camera = Camera(self.box,
                        viewWidth=sizeX*1.5, viewHeight=sizeY*1.5,
                        x=(sizeX / 2), y=(sizeY / 2), z=(sizeZ / 2),
                        perspective=True)
        cameraView = CameraViewWidget(None, camera)
        
        
        self.camera = camera
        self.cameraView = cameraView
        
        self.cameraView.ballSelected.connect(self.ballSelected)
    
    def initWidgets(self):
        self.initCamera()
        
        self.hitButton = QPushButton("Hit")
        self.hitButton.clicked.connect(self.hitEvent)
        
        self.forceSlider = QSlider(Qt.Horizontal)
        self.forceSlider.setTickInterval(1)
        self.forceSlider.valueChanged.connect(self.hitForceChangeEvent)
        
        cameraLayout = QHBoxLayout()
        cameraLayout.setContentsMargins(0, 0, 0, 0)
        cameraLayout.addWidget(self.cameraView)
        
        controlsLayout = QHBoxLayout()
        controlsLayout.setContentsMargins(0, 0, 0, 0)
        controlsLayout.addWidget(self.hitButton)
        controlsLayout.addWidget(self.forceSlider)
        
        mainLayout = QVBoxLayout()
        cameraLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addLayout(cameraLayout)
        mainLayout.addLayout(controlsLayout)
        
        self.setLayout(mainLayout)
    
    def hitEvent(self, event):
        if self.selectedBall:
            print(event)
            self.selectedBall.hit(self.hitDirection, self.hitForce)
            self.selectedBall = None
    
    def hitForceChangeEvent(self, value):
        self.hitForce = value / 10
        print(self.hitForce)
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_A:
            self.spectatorSpeedDirection[0] -= 1
        if key == Qt.Key_D:
            self.spectatorSpeedDirection[0] += 1
        if key == Qt.Key_Q:
            self.spectatorSpeedDirection[1] -= 1
        if key == Qt.Key_E:
            self.spectatorSpeedDirection[1] += 1
        if key == Qt.Key_S:
            self.spectatorSpeedDirection[2] -= 1
        if key == Qt.Key_W:
            self.spectatorSpeedDirection[2] += 1
        
        if key == Qt.Key_Shift:
            self.spectatorSpeedValue = 4
    
    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_A:
            self.spectatorSpeedDirection[0] += 1
        if key == Qt.Key_D:
            self.spectatorSpeedDirection[0] -= 1
        if key == Qt.Key_Q:
            self.spectatorSpeedDirection[1] += 1
        if key == Qt.Key_E:
            self.spectatorSpeedDirection[1] -= 1
        if key == Qt.Key_S:
            self.spectatorSpeedDirection[2] += 1
        if key == Qt.Key_W:
            self.spectatorSpeedDirection[2] -= 1
        
        if key == Qt.Key_Shift:
                    self.spectatorSpeedValue = 1
    
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
        
        self.lastMousePos = [x, y]
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastMousePos = None
    
    def ballSelected(self, ball, camera):
        if camera.perspective:
            direction = (planimetry.Vector(ball.sphere.x, ball.sphere.y, ball.sphere.z) -
                       planimetry.Vector(camera.x, camera.y, camera.z))
            if abs(direction) == 0:
                return
            
            self.hitDirection = direction * (1 / abs(direction))
        else:
            x, y, z = rotate(0, 0, 1, camera.rotOX, camera.rotOY, camera.rotOZ, reverse=True)
            f = 5
            
            self.hitDirection = planimetry.Vector(x, y, z)
        self.selectedBall = ball
    
    def moveSpectator(self):
        x, y, z = self.spectatorSpeedDirection
        v = self.spectatorSpeedValue
        self.camera.moveLocal(x * v, y * v, z * v)

    def timerEvent(self, event):
        self.moveSpectator()
        
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