import sys
from PyQt5.Qt import*
import phisi as physics
import plani as planimetry
from render import *
from gameController import *

oldBall = physics.Ball

class Ball(oldBall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.selectedColor = (0, 190, 0)
        self.diselectedColor = (0, 0, 0)
        
        self.fillColor = (160, 160, 160)
        self.borderColor = self.diselectedColor
        
        self.canBeSelected = False
    
    def select(self):
        self.borderColor = self.selectedColor
    
    def diselect(self):
        self.borderColor = self.diselectedColor

physics.Ball = Ball


class CommunicationGameEnd(QObject):
    gameEnded = pyqtSignal()


class BilliardsWidget(QWidget):
    def __init__(self, parent=None, gameControllerClass=BaseGameController):
        super().__init__(parent)
        
        self.box = physics.Box(500, 500, 500, [], [], 0.005, 0.005)
        
        self.initGameMode(gameControllerClass)
        
        if parent is None:
            self.initWindowGeometry()
        self.initWidgets()
        
        self.spectatorSpeedDirection = [0, 0, 0]
        self.spectatorSpeedValue = 1
        self.spectatorRotationSpeed = 1
        
        self.selectedBall = None
        self.hitDirection = planimetry.Vector(0, 0, 0)
        self.hitForce = 0
        
        self.lastMousePos = None
        
        self.gameController._gameInit()
        self.gameController._gameStart()
        
        self.timer = QBasicTimer()
        self.timer.start(10, self)
    
    def initWindowGeometry(self):
        self.resize(1000, 500)
    
    def initGameMode(self, gameControllerClass):
        self.gameController = gameControllerClass(self)
        
        self.box.ballHitCallback = self.gameController._ballHitEvent
        self.box.wallHitCallback = self.gameController._wallHitEvent
        self.box.inHoleCallback = self.gameController._inHoleEvent
        
        self.isNewTurn = False
        
    def initCamera(self):
        sizeX = self.box.sizeX
        sizeY = self.box.sizeY
        sizeZ = self.box.sizeZ
        sizeMax = max(sizeX, sizeY, sizeZ)
        
        camera = Camera(self.box,
                        viewWidth=sizeMax*1.5, viewHeight=sizeMax*1.5,
                        x=(sizeX / 2), y=(sizeY / 2), z=0,
                        perspective=True)
        
        cameraView = CameraViewWidget(None, camera)
        
        
        self.camera = camera
        self.cameraView = cameraView
        
        self.cameraView.ballSelected.connect(self.ballSelected)
    
    def initWidgets(self):
        self.initCamera()
        
        self.messageLabel = QLabel()
        self.messageLabel.setAlignment(Qt.AlignHCenter)
        self.messageLabel.setMaximumHeight(40)
        self.gameController.setMessageCallback = self.messageLabel.setText
        
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
        
        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.gameController._gameEnd)
        
        spacer = QSpacerItem(0, 30)
        
        mainGrid = QGridLayout()
        mainGrid.setContentsMargins(0, 0, 0, 0)
        #mainGrid.setSpacing(0);
        
        cameraLayout.setContentsMargins(0, 0, 0, 0)
        mainGrid.addWidget(self.messageLabel, 0, 0)
        mainGrid.addLayout(cameraLayout, 1, 0)
        mainGrid.addLayout(controlsLayout, 2, 0)
        mainGrid.addItem(spacer, 3, 0)
        mainGrid.addWidget(self.exitButton, 4, 0)
        
        self.setLayout(mainGrid)
    
    def ballSelected(self, ball, camera):
        if self.isNewTurn or not ball.canBeSelected:
            return
        
        if self.selectedBall:
            self.selectedBall.diselect()
        
        if camera.perspective:
            direction = (planimetry.Vector(ball.sphere.x, ball.sphere.y, ball.sphere.z) -
                       planimetry.Vector(camera.x, camera.y, camera.z))
            if abs(direction) == 0:
                return
            
            hitDirection = direction * (1 / abs(direction))
        else:
            x, y, z = rotate(0, 0, 1, camera.rotOX, camera.rotOY, camera.rotOZ, reverse=True)
            
            hitDirection = planimetry.Vector(x, y, z)
        
        self.hitDirection = hitDirection
        self.selectedBall = ball
        
        ball.select()
    
    def hitEvent(self, event):
        if self.selectedBall:
            self.selectedBall.hit(self.hitDirection, self.hitForce)
            self.selectedBall.diselect()
            self.selectedBall = None
            
            self.isNewTurn = True
    
    def hitForceChangeEvent(self, value):
        self.hitForce = value / 10
    
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
        if key == Qt.Key_Control:
            self.spectatorRotationSpeed = 0.3
        
        if key == Qt.Key_P:
            self.camera.perspective ^= 1
        
        if key == Qt.Key_C:
            self.cameraView.drawCenter ^= 1
    
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
        if key == Qt.Key_Control:
            self.spectatorRotationSpeed = 1
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastMousePos = [event.x(), event.y()]
    
    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton or not self.lastMousePos:
            return
        
        x, y = event.x(), event.y()
        lastX, lastY = self.lastMousePos
        dx, dy = x - lastX, y - lastY
        self.camera.rotOX -= dy / 100 * self.spectatorRotationSpeed
        self.camera.rotOY -= dx / 100 * self.spectatorRotationSpeed
        
        self.lastMousePos = [x, y]
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastMousePos = None
    
    def moveSpectator(self):
        x, y, z = self.spectatorSpeedDirection
        v = self.spectatorSpeedValue
        self.camera.moveLocal(x * v, y * v, z * v)

    def timerEvent(self, event):
        self.moveSpectator()
        
        self.box.movement()
        
        if self.isNewTurn:
            for ball in self.box.balls:
                if ball.speed.lenSq() != 0 and not ball.isInHole():
                    break
            else:
                self.gameController._gameTurn()
                self.isNewTurn = False
        
        self.update()