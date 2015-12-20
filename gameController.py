class BallHitEvent:
    def __init__(self, ball1, ball2):
        self.balls = (ball1, ball2)
    
    def __str__(self):
        return "BallHitEvent. Balls: %s, %s"%self.balls

class WallHitEvent:
    def __init__(self, ball):
        self.ball = ball
    
    def __str__(self):
        return "WallHitEvent. Ball: %s"%(self.ball)

class InHoleEvent:
    def __init__(self, ball, hole):
        self.ball = ball
        self.hole = hole
    
    def __str__(self):
        return "InHoleEvent. Ball, Hole: %s, %s"%(self.ball, self.hole)

class BaseGameController:
    name = "Base"
    description = "Base game mode (controller)"
    
    def __init__(self, billiards):
        self.billiards = billiards
        
        self.events = []
        self.gameEndCallback = None
        self.setMessageCallback = None
    
    def ballHitEvent(self, ball1, ball2):
        self.events.append(BallHitEvent(ball1, ball2))
    
    def wallHitEvent(self, ball):
        self.events.append(WallHitEvent(ball))
    
    def inHoleEvent(self, ball, hole):
        self.events.append(InHoleEvent(ball, hole))
    
    def wipeEvents(self):
        self.events = []
    
    def _gameInit(self):
        self.box = self.billiards.box
        self.camera = self.billiards.camera
        
        self.gameInit()
    
    def _gameStart(self):
        self.gameStart()
    
    def _gameTurn(self):
        self.gameTurn()
        self.wipeEvents()
    
    def _gameEnd(self):
        if self.gameEndCallback:
            self.gameEndCallback()
    
    def gameInit(self):
        pass
    
    def gameStart(self):
        pass
    
    def gameTurn(self):
        pass
    
    def setMessage(self, message):
        if self.setMessageCallback:
            self.setMessageCallback(message)