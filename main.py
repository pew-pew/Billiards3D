import sys
from PyQt5.Qt import *
import phisi as physics
import plani as planimetry
from render import *
from billiards import *

class Game(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1000, 500)
        
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
        
        vbox = QVBoxLayout()
        self.billiards = BilliardsWidget(None, box)
        vbox.addWidget(self.billiards)
        self.setLayout(vbox)
            
    def keyPressEvent(self, event):
        return self.billiards.keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        return self.billiards.keyReleaseEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Game()
    widget.show()
    sys.exit(app.exec_())