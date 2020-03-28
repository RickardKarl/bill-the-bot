from tictactoe.board import Board
from tictactoe.simulation import simulate

if __name__ == "__main__":
    
    """
    game = Board()
    print(game)
    game.setPosition(1,2,1)
    print(game)
    print(game.checkWinner())
    game.setPosition(1,0,1)
    game.setPosition(1,1,1)
    print(game)
    print(game.checkWinner())
    """

    agent1, _ = simulate()
    agent2, _ = simulate(agent1=agent1, use_trainer1=True)
    agent3, _ = simulate(agent1=agent2, use_trainer1=True)