from tictactoe.board import Board
from tictactoe.simulation import simulate
from tictactoe.agent import Agent

if __name__ == "__main__":

    # Train two agents against each other and save it in playerX.pkl
    iterations = 250000
    agent1, agent2 = simulate(iterations, explore_only=False, save_agent1="playerX.pkl")
