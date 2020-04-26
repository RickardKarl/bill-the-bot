import tkinter as tk
import random 
import time
import numpy as np

from tictactoe.board import Board
from tictactoe.agent import Agent
from tictactoe.simulation import simulate

playerX = Board.playerX
playerO = Board.playerO
agent_save = "playerX.pkl"

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Tic-tac-toe")
        self.master.minsize(300, 300)
    
        # Start game
        self.board = Board(rows=3, cols=3, win_threshold=3)
        self.current_player = playerX if (random.random() < 0.5) else playerO
        
        # Train agent and assign it to this game
        print("Preparing agent")
        #self.agent, agent2 = simulate(iterations=5000, exploration=True)
        #self.agent.assignState(self.board)
        self.agent = Agent(playerX, self.board, load_trainer=agent_save)
        self.agent_symbol = self.agent.symbol

        # Create widgets
        self.createBoard(self.board)

        if self.current_player == self.agent_symbol:
            self.agentMove()

        self.pack(fill="both")

    def createBoard(self, board):

        # Text label
        self.info_label = tk.Label(self, text = "Player {}'s turn".format("X" if self.current_player == playerX else "O") )


        # Create buttons
        self.button00 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(0,0))
        self.button01 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(0,1))
        self.button02 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(0,2))

        self.button10 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(1,0))
        self.button11 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(1,1))
        self.button12 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(1,2))

        self.button20 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(2,0))
        self.button21 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(2,1))
        self.button22 = tk.Button(self, height = 4, width = 8, text=' ', font='Times 20 bold', bg='gray', fg='white', command = lambda : self.playMove(2,2))

        self.reset_button = tk.Button(self, text = "Reset", command = self.resetGame)
        self.Q_button = tk.Button(self, text="Display Q values", command = self.displayQ, relief='raised')

        # Insert to grid
        self.info_label.grid(row = 0, column = 1)

        self.button00.grid(row = 1, column = 0)
        self.button01.grid(row = 1, column = 1)
        self.button02.grid(row = 1, column = 2)

        self.button10.grid(row = 2, column = 0)
        self.button11.grid(row = 2, column = 1)
        self.button12.grid(row = 2, column = 2)
        
        self.button20.grid(row = 3, column = 0)
        self.button21.grid(row = 3, column = 1)
        self.button22.grid(row = 3, column = 2)

        self.reset_button.grid(row = 4, column = 1)
        self.Q_button.grid(row = 4, column = 2)


    def getText(self, x, y):
        value = self.board.getPosition(x, y)
        if value == playerX:
            return "X"
        elif value == playerO:
            return "O"
        else:
            return " "
    
    def getQValue(self, x, y):
        value = self.getText(x,y)
        if value == " ":
            action_hash = self.agent.getActionHash(np.asarray([x,y]))
            state_hash = self.board.getStateHash()
            Q = self.agent.trainer.getValueQ(state_hash, action_hash)
            return "{:.2f}".format(Q)
        else:
            return value

    def updateText(self):
        
        self.info_label.configure(text="Player {}'s turn".format("X" if self.current_player == playerX else "O"))

        self.button00.configure(text=self.getText(0,0), state=tk.ACTIVE)
        self.button01.configure(text=self.getText(0,1), state=tk.ACTIVE)
        self.button02.configure(text=self.getText(0,2), state=tk.ACTIVE)
        self.button10.configure(text=self.getText(1,0), state=tk.ACTIVE)
        self.button11.configure(text=self.getText(1,1), state=tk.ACTIVE)
        self.button12.configure(text=self.getText(1,2), state=tk.ACTIVE)
        self.button20.configure(text=self.getText(2,0), state=tk.ACTIVE)
        self.button21.configure(text=self.getText(2,1), state=tk.ACTIVE)
        self.button22.configure(text=self.getText(2,2), state=tk.ACTIVE)

        self.reset_button.configure(state=tk.ACTIVE)

    def displayQ(self):

        if self.Q_button.config('relief')[-1] == 'sunken':
            self.updateText()
            self.Q_button.configure(text="Display Q values", relief='raised')
        else:
            self.button00.configure(text=self.getQValue(0,0), state=tk.DISABLED)
            self.button01.configure(text=self.getQValue(0,1), state=tk.DISABLED)
            self.button02.configure(text=self.getQValue(0,2), state=tk.DISABLED)
            self.button10.configure(text=self.getQValue(1,0), state=tk.DISABLED)
            self.button11.configure(text=self.getQValue(1,1), state=tk.DISABLED)
            self.button12.configure(text=self.getQValue(1,2), state=tk.DISABLED)
            self.button20.configure(text=self.getQValue(2,0), state=tk.DISABLED)
            self.button21.configure(text=self.getQValue(2,1), state=tk.DISABLED)
            self.button22.configure(text=self.getQValue(2,2), state=tk.DISABLED)
            self.reset_button.configure(state=tk.DISABLED)

            self.Q_button.configure(text="Hide Q values", relief='sunken')




    def playMove(self, x, y):
        
        # Raise error because position is non-empty
        if self.board.getPosition(x,y) == playerX or self.board.getPosition(x,y) == playerO:
            print("Error")
        else:
            # Update board
            self.board.setPosition(x, y, self.current_player)

            # Swap player
            if self.current_player == playerX:
                self.current_player = playerO
            else:
                self.current_player = playerX

            # Update text
            self.updateText()

            # Check if game has ended
            winner = self.board.checkWinner()
            if winner != 0 or self.board.checkGameEnded():
                self.endGame()

            elif self.current_player == self.agent_symbol:
                self.agentMove()

    def agentMove(self):
        move = self.agent.getBestAction()
        time.sleep(random.random()*1 + 0.5)
        self.playMove(move[0], move[1])

    def endGame(self):
        winner = self.board.checkWinner()
        if winner == playerX:
            self.info_label.configure(text = "Player X won!") 
        elif winner == playerO:
            self.info_label.configure(text = "Player O won!") 
        else:
            self.info_label.configure(text = "Game tied") 

    def resetGame(self):
        self.board.resetGame()
        self.current_player = playerX if (random.random() < 0.5) else playerO
        if self.current_player == self.agent_symbol:
            self.agentMove()
        self.updateText()



if __name__ == "__main__":
    Application()
    tk.mainloop()
