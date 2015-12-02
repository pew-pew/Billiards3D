import sys
from PyQt5.Qt import *
import phisi as physics
import plani as planimetry
from collections import deque


class BilliardsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.initBox()
        self.initBaseProperties()
        
        self.timer = QBasicTimer()
        self.timer.start(10, self)
    
    def initBaseProperties(self):
        self.setFixedSize(300, 300)
        self.move(300, 300)
    
    def initBox(self):
        sizeX, sizeY, sizeZ = 300, 300, 300
        
        #             physics.Ball(x, y, z, R, m, vx, vy, vz)
        self.balls = [physics.Ball(250, 130, 150, 20, 1, 1.5, 0.3, 0),
                      physics.Ball(200, 160, 150, 20, 1, 1, 2, 0),
                      ]
        self.holes = []
        self.box = physics.Box(300, 300, 300, self.balls, self.holes, 0, 0)
    
    def drawBalls(self):
        painter = QPainter(self)
        for ball in self.balls:
            sp = ball.sphere
            x, y, z, r = sp.x, sp.y, sp.z, sp.R
            
            rect = QRect(x - r, y - r, r * 2, r * 2)
            painter.drawEllipse(rect)
    
    def paintEvent(self, event):
        physics.Box.movement(self.box)
        self.drawBalls()
    
    def timerEvent(self, event):
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BilliardsWidget()
    widget.show()
    sys.exit(app.exec_())