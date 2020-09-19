
from tictactoe.agent import Agent
from tictactoe.board import Board
from tictactoe.learning import Trainer

from tqdm import tqdm
import random

player1_symbol = Board.playerX
player2_symbol = Board.playerO

def simulate(iterations, explore_only = False, save_agent1 = None):
    """
        iterations (int)
        explore_only (bool) - If true, then only explore.
                              Else,  follow an epsilon-greedy policy that lowers the probability to explore over time.
    """

    # Construct game board
    game = Board()
    exploration_probability = 1
    
    # Initialize players
    agent1 = Agent(player1_symbol, game)
    agent2 = Agent(player2_symbol, game)

    # Counters for wins of each agent and total number of games
    nbr_wins_agent1 = 0
    nbr_wins_agent2 = 0
    nbr_games = 0

    # Pick current player
    current_player = player1_symbol

    # Epsilon-greedy 
    exploration_probability = 1.0

    # Start iterations
    for i in tqdm(range(iterations)):

        # Check if games has ended, reset if True
        if game.checkGameEnded():
            nbr_games += 1
            game.resetGame()
            agent1.updatePossibleActions()
            agent2.updatePossibleActions()

        # Check who is the current player 
        if current_player == agent1.symbol:
            a = agent1
        else:
            a = agent2

        # Explore
        if explore_only is True or random.random() < exploration_probability:
            a.performRandomAction(updateQ=True)
        # Exploit
        else:
            best_action = a.getBestAction()
            a.performAction(best_action, updateQ=(True))

        # Reduce probability to explore during training
        # Do not remove completely
        if exploration_probability > 0.2:
            exploration_probability -= 1/iterations

        # Check if there is a winner
        winner = game.checkWinner() # Returns 0 if there is no winner
        if winner != 0:

            # Reset game and retrieve 
            nbr_games += 1
            game.resetGame()

            # Add to count for corresponding winner
            if winner == agent1.symbol:
                nbr_wins_agent1 += 1
            else:
                nbr_wins_agent2 += 1
        
        # Swap player
        if current_player == player1_symbol:
            current_player = player2_symbol
        else:
            current_player = player1_symbol

        
    # Print outcome
    print(nbr_wins_agent1, nbr_wins_agent2, nbr_games)    
    print("Win percentage: Agent 1 {:.2%}, Agent 2 {:.2%}.".format(nbr_wins_agent1/nbr_games, nbr_wins_agent2/nbr_games))

    if save_agent1 is not None:
        print("Saved trainer of agent 1 to {}".format(save_agent1))
        agent1.saveTrainer(save_agent1)

    # Return agents
    return agent1, agent2


