import sys
from PyQt5.Qt import *
from billiards import *
from gameController import *
from importer import *
from gameModeSelection import *

class Game(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 600)
        
        self.billiardsWidget = None
        
        self.gameModeSelectionWidget = GameModeSelectionWidget(self)
        self.gameModeSelectionWidget.gameModeChosen.connect(self.playBeginEvent)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.gameModeSelectionWidget)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.stack)
        vbox.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(vbox)
    
    def playBeginEvent(self, gameController):
        self.billiardsWidget = BilliardsWidget(None, gameController)
        self.billiardsWidget.gameController.gameEndCallback = self.playEndEvent
        self.stack.addWidget(self.billiardsWidget)
        self.stack.setCurrentIndex(1)
    
    def playEndEvent(self):
        self.stack.removeWidget(self.billiardsWidget)
        
    def keyPressEvent(self, event):
        if self.billiardsWidget is None:
            return        
        return self.billiardsWidget.keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        if self.billiardsWidget is None:
            return
        return self.billiardsWidget.keyReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Game()
    widget.show()
    sys.exit(app.exec_())