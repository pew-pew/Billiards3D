import sys
import os
import imp
from gameController import *


def importControllers():
    gameControllers = []
    
    files = os.listdir("Game modes/")
    for fileName in files:
        if fileName[-3:] != ".py":
            continue
        
        module = imp.load_source("fileName", "Game modes/" + fileName)
        controller = module.GameController
        controller.name = module.name
        controller.description = module.description
        
        gameControllers.append(controller)
    
    return gameControllers