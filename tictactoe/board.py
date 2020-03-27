import numpy as np

class Board:
    """ Class that represents the game board of Tic Tac Toe """

    def __init__(self, rows = 3, cols = 3, win_threshold = 3):
        
        self.state = np.zeros((rows, cols))
        self.rows = rows
        self.cols = cols
        self.win_threshold = win_threshold

    def getState(self):
        """ Get state of game """
        return self.state
    
    def getPosition(self, x, y):
        """ Get state at position (x,y) """
        return self.state[x,y]

    def setPosition(self, x, y, value):
        """  Set state at position (x,y) with value """
        self.state[x,y] = value

    def getAvailablePos(self):
        """  Get state positions that have no value (non-zero) """
        return self.state == 0

    def getStateHash(self):
        """  Get hash key of state """
        return str(self.state)

    def checkWinner(self):
        """  Get winner, if one exists """
        symbols = np.unique(self.state)

        for sym in symbols:
            positions = (self.state == sym)
