
from tictactoe.agent import Agent
from tictactoe.board import Board
from tictactoe.learning import Trainer

import numpy as np
from tqdm import tqdm

player1_symbol = 1
player2_symbol = -1 

def simulate(iterations = 5000):

    # Construct game board
    game = Board()

    # Construct agents
    agent1 = Agent(player1_symbol, game)
    agent2 = Agent(player2_symbol, game)

    # Counters for wins of each agent and total number of games
    nbr_wins_agent1 = 0
    nbr_wins_agent2 = 0
    nbr_games = 0

    # Pick current player
    current_player = player1_symbol

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


        # Pick random actions for agent out of possible actions
        possible_actions = a.getPossibleActions()
        random_idx = np.random.choice(possible_actions.shape[0])
        action = possible_actions[random_idx]

        # Perform move which updates Q-value for that state-action pair
        a.performAction(action, updateQ=True)

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


    
    print("Win percentage: Agent 1 {:.2%}, Agent 2 {:.2%}.".format(nbr_wins_agent1/nbr_games, nbr_wins_agent2/nbr_games))
    
    # Return agents
    return agent1, agent2


