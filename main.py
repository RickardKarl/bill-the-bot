from tictactoe.board import Board
from tictactoe.simulation import simulate
from tictactoe.agent import Agent

if __name__ == "__main__":

    # Train two agents against each other
    agent1, agent2 = simulate(exploration=True, iterations=1000000, save_agent1="playerX.pkl")
    agent1, agent2 = simulate(agent1=agent1, exploration=False, iterations=5000, eval=True)
    

"""
    Without combining knowledge
    Iterations: 500,000 10,000
    Winrate:    79.67%  61.73

"""