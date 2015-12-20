import sys
from PyQt5.Qt import *
from importer import *

class CommunicationGameModeChosen(QObject):
    gameModeChosen = pyqtSignal(type)

class GameModeSelectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is None:
            self.resize(300, 300)
        
        self.communication = CommunicationGameModeChosen()
        self.gameModeChosen = self.communication.gameModeChosen
        
        self.initWidgets()
        self.initLayout()
        
        self.currentGameMode = None
    
    def initWidgets(self):
        gameModesListView = QListView()
        gameModesItemModel = QStandardItemModel(gameModesListView)
        gameModesListView.setModel(gameModesItemModel)
        
        gameModes = importControllers()
        for mode in gameModes:
            item = QStandardItem(mode.name)
            item.setEditable(False)
            gameModesItemModel.appendRow(item)
        
        nameLabel = QLabel("Name:")
        gameModeNameLabel = QLabel("")
        
        descriptionLabel = QLabel("Description:")
        gameModeDescriptionLabel = QLabel("")
        
        playButton = QPushButton("Play!")
        
        gameModesListView.clicked.connect(self.itemSelectedEvent)
        playButton.clicked.connect(self.playButtonPushEvent)
        
        self.gameModesListView = gameModesListView
        self.gameModesItemModel = gameModesItemModel
        self.gameModes = gameModes
        
        self.nameLabel = nameLabel
        self.gameModeNameLabel = gameModeNameLabel
        
        self.descriptionLabel = descriptionLabel
        self.gameModeDescriptionLabel = gameModeDescriptionLabel
        self.playButton = playButton
    
    def initLayout(self):
        grid = QGridLayout()
        
        grid.addWidget(self.gameModesListView, 0, 0, -1, 1)
        
        grid.addWidget(self.nameLabel, 0, 1, Qt.AlignTop)
        grid.addWidget(self.descriptionLabel, 1, 1, Qt.AlignTop)
        
        grid.addWidget(self.gameModeNameLabel, 0, 2, Qt.AlignTop)
        grid.addWidget(self.gameModeDescriptionLabel, 1, 2, Qt.AlignTop)
        grid.addWidget(self.playButton, 2, 1, 1, 2)
        
        self.setLayout(grid)
    
    def itemSelectedEvent(self, item):
        pos = item.row()
        gameMode = self.gameModes[pos]
        self.gameModeSelected(gameMode)
    
    def gameModeSelected(self, gameMode):
        self.currentGameMode = gameMode
        self.gameModeNameLabel.setText(gameMode.name)
        self.gameModeDescriptionLabel.setText(gameMode.description)
    
    def playButtonPushEvent(self):
        self.gameModeChosen.emit(self.currentGameMode)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = GameModeSelectionWidget()
    widget.show()
    sys.exit(app.exec_())